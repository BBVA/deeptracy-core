import os
import random
import docker
import tempfile

from typing import List
from contextlib import contextmanager


@contextmanager
def run_in_docker(docker_image: str,
                  *,
                  environment_vars: List[str] = None,
                  command: str = None,
                  working_dir: str ="/opt/app") -> str:
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
    :param environment_vars: List with additional environment vars
    :param command: additional command to pass to docker image when it runs
    :param working_dir: working directory for the docker app
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

        result_file = "".join(str(random.randint(0, 9))
                              for _ in range(30))
        host_result_file = os.path.join(tmp_dir, result_file)
        container_result_file = os.path.join(working_dir, result_file)

        # Choice volumes
        docker_volumes = {
            tmp_dir: {
                'bind': working_dir,
                'mode': 'rw'
            }
        }

        # --------------------------------------------------------------------------
        # Build function call options
        # --------------------------------------------------------------------------
        envs = environment_vars or []
        envs.extend([
            "OUTPUT_FILE={}".format(container_result_file)
        ])

        # Run content inside docker
        docker_client.containers.run(
            image=docker_image,
            command=command,
            remove=True,
            environment=envs,
            working_dir=working_dir,
            volumes=docker_volumes
        )

        # Read result file
        try:
            with open(host_result_file, "r") as f:
                yield f.read()
        except IOError:
            yield ""
