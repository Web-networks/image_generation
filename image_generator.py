import re
from typing import List, BinaryIO
import sys
import json

import docker


def build_image(client: docker.api.client.APIClient, dockerfile: BinaryIO,
                pip_libraties: List[str],
                tag: str) -> docker.models.images.Image:
    image, logs = client.images.build(
        fileobj=dockerfile,
        buildargs={
            "PIP_LIBRARIES": pip_libraries,
        },
        encoding="utf-8",
        rm=True,
        forcerm=True,
        tag=tag
    )
    for log in logs:
        sys.stdout.write(json.dumps(log) + "\n")
    return image


if __name__ == '__main__':
    # tag will be set as some id from storage later
    client = docker.from_env()
    tag = "testimage"
    pip_libraries = sys.stdin.read().strip()
    with open("Dockerfile.code_editor", "rb") as dockerfile:
        image = build_image(
            client, 
            dockerfile, 
            pip_libraries,
            tag
        )
    # docker.push(regisry_host, tag)

    # test it
    result = client.containers.run(
        tag, 
        command=sys.argv[1],
        volumes={sys.argv[2]: {"bind": "/home", "mode": "rw"}}
    )

    print("\n" + result.decode("utf-8"))
