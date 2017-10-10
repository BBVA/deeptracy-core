# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import docker
import tempfile

from typing import List
from contextlib import contextmanager


def get_plugin_image(plugin_path: str = None) -> str:
    import inspect
    import os.path as op

    def get_origin_file() -> str:
        for x in range(100):
            try:
                path = inspect.stack()[x][1]
                if "plugins" in path:
                    return path

            except IndexError:
                return ""

    plugin_path = plugin_path or op.dirname(get_origin_file())

    # Get docker version
    docker_version = open(op.abspath(op.join(plugin_path, "VERSION")),
                          "r").read().replace("\n", "")

    docker_image = open(op.abspath(op.join(plugin_path,
                                           "IMAGE_NAME")),
                        "r").read().replace("\n", "")

    return "bbvalabs/{}:{}".format(docker_image, docker_version)


@contextmanager
def run_in_docker(docker_image: str,
                  source_code_path: str,
                  *,
                  environment_vars: List[str] = None,
                  command: str = None,
                  result_path: str ="/tmp/results") -> str:
    """
    This context manager launch a Docker image and return the content of file
    assigned to environment variable 'OUTPUT_FILE'.

    The basic execution simulates this launch:

    > docker run --rm -w WORKING_DIR -e OUTPUT_FILE="/tmp/auto_generated_file" IMAGE [CMD]

    Where:

        - OUTPUT_FILE: contains a auto-generated file name in your system where
          you must dump your results
        - CMD: Are the extra parameter for your image
        - WORKING_DIR: by default is '/opt/app'

    When the execution finishes, context manager return the content of
    OUTPUT_FILE as a string.

    Example:

    >>> CMD = "sh -c \"echo hello > \$OUTPUT_FILE\""
    >>> with run_in_docker("busybox", working_dir="/tmp", command=CMD) as f:
        print(f)
    hello

    :param docker_image: docker image from DockerHub
    :param source_code_path: absolute path for source code to analyze
    :param environment_vars: List with additional environment vars
    :param command: additional command to pass to docker image when it runs
    :param result_path: path for results of execution
    :rtype: str
    """

    #
    # Create temporal directory in the local host.
    #
    # We use dir="/tmp" because in OSX, TemporaryDirectory function create the
    # temporal dir in path "/var/..." and, by default, Docker hasn't permission
    # to mount this directory, raising a error like that:
    #
    #   The path /var/folders/_h/b5wqbhtn4zvcmsshf8nv1kcr0000gn/T/deeptracykyoc
    #   is not shared from OS X and is not known to Docker.
    #   You can configure shared paths from Docker ->
    #      Preferences... -> File Sharing.
    #   See https://docs.docker.com/docker-for-mac/osxfs/#namespaces for
    #      more info.
    # -------------------------------------------------------------------------
    with tempfile.TemporaryDirectory(prefix="deeptracy",
                                     dir="/tmp") as tmp_dir:

        docker_client = docker.from_env()

        result_file_name = "".join(str(random.randint(0, 9))
                                   for _ in range(30))
        host_result_file = os.path.join(tmp_dir, result_file_name)

        # Choice volumes
        docker_volumes = {
            tmp_dir: {
                'bind': result_path,
                'mode': 'rw'
            },
            source_code_path: {
                'bind': "/opt/app",
                'mode': 'ro'
            },
        }

        # --------------------------------------------------------------------------
        # Build function call options
        # --------------------------------------------------------------------------
        envs = environment_vars or []
        envs.extend([
            # "OUTPUT_FILE={}".format(container_result_file)
            "OUTPUT_FILE={}".format(result_file_name)
        ])

        # Run content inside docker
        docker_client.containers.run(
            image=docker_image,
            remove=True,
            command=command,
            environment=envs,
            volumes=docker_volumes
        )

        # Read result file
        with open(host_result_file, "r") as f:
            yield f.read()
