import re
from typing import List, BinaryIO
import sys
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


def build_image(client: docker.api.client.APIClient, dockerfile: BinaryIO,
                pip_libraties: List[str],
                tag: str) -> docker.models.images.Image:
    image, logs = client.images.build(
        fileobj=dockerfile,
        buildargs={
            "PIP_LIBRARIES": " ".join(pip_libraries),
        },
        encoding="urf-8",
        rm=True,
        forcerm=True,
        tag=tag
    )
    for log in logs:
        sys.stderr.write(json.dumps(log) + "\n")
    return image


if __name__ == '__main__':
    pip_libraries = ["numpy", "flask"]
    check_for_restricted_dependencies(pip_libraries)
    pip_libraries = remove_default_dependencies(pip_libraries)
    # tag will be set as some id from storage later
    client = docker.from_env()
    tag = "testimage"
    with open("Dockerfile.code_editor", "rb") as dockerfile:
        image = build_image(
            client, 
            dockerfile, 
            pip_libraries,
            tag
        )
    # docker.push(regisry_host, tag)

    # test it
    client.containers.run(
        tag, 
        network="host",
        environment={"JUPYTER_TOKEN": "abcd"},
        ports={"8888": "8888"}
    )
