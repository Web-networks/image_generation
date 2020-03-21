import re
from typing import List
import sys
import io
import json

import docker

import module_lists


def parse_dependencies(file_content: str) -> List[str]:
    """
        :param file_content - content of file to be parsed
        :return list of strings

        Example file.py:
            import numpy
            from pandas import ndarray,\
                kekule
            import matplotlib as plt

            def f():
                from re import findall
                import ku_le42
        Returns:
            ['numpy', 'pandas', 'matplotlib', 're', 'ku_le42']


    """
    libraries = []
    for line in file_content.split("\n"):
        library = re.match(r'^\s*import\s([\w\d_]+)\s', line)
        if library and library.group(1):
            libraries.append(library.group(1))
        else:
            library = re.match(r'^\s*from\s([\w\d_]+)\simport', line)
            if library and library.group(1):
                libraries.append(library.group(1))
    return libraries


def check_for_restricted_dependencies(dependencies: List[str]) -> None:
    """
        :param dependencies - list of modules to import

        Throws an error if any of dependencies is not allowed to import


    """
    for dependency in dependencies:
        assert dependency not in module_lists.restricted_dependencies, \
            "{} is not allowed to import".format(dependency)


def remove_default_dependencies(dependencies: List[str]) -> List[str]:
    """
        :param dependencies - list of modules to import
        :return list without default modules


    """
    return list(filter(
        lambda x: x not in module_lists.default_dependencies,
        dependencies
    ))


def create_dockerfile(dependencies: List[str], base_image: str) -> str:
    """
        :paran dependencies - list of modules to install
        :return dockerfile for image with installed dependencies

    """

    dockerfile = "FROM {}\n".format(base_image)
    if dependencies:
        dockerfile += "RUN pip install {}\n".format(", ".join(dependencies))
    return dockerfile


def build_image(client: docker.api.client.APIClient,
                dockerfile: str, tag: str) -> docker.models.images.Image:
    image, logs = client.images.build(
        fileobj=io.BytesIO(dockerfile.encode("utf-8")),
        encoding="utf-8",
        rm=True,
        forcerm=True,
        tag=tag
    )
    for log in logs:
        sys.stderr.write(json.dumps(log) + "\n")
    return image


if __name__ == '__main__':
    file_content = sys.stdin.read()
    dependencies = parse_dependencies(file_content)
    check_for_restricted_dependencies(file_content)
    dependencies = remove_default_dependencies(dependencies)
    dockerfile = create_dockerfile(dependencies, "python:3.8.2-slim")
    # tag will be set as some id from storage later
    client = docker.from_env()
    tag = "testimage"
    image = build_image(client, dockerfile, tag)
    # docker.push(regisry_host, tag)

    # test it
    print(client.containers.run(tag, 'python -c "{}"'.format(file_content)))
