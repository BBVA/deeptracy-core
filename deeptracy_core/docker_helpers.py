import docker
import tempfile


# os.system('docker run -v $(pwd):/opt/app -e OUTPUT_FILE={} {}'
#               .format(OUTPUT_FILE, DOCKER_IMAGE))
def run_in_docker(docker_image: str,
                  image_parameters: str):

    # Create temporal directory in the local host
    with tempfile.TemporaryDirectory(prefix="deeptracy") as tmp_dir:

        docker_client = docker.from_env()

        # Choice volumes
        docker_volumes = {
            tmp_dir: {
                'bind': '/opt/app',
                'mode': 'rw'
            }
        }

        # Run content inside docker
        docker_client.containers.run(
            docker_image,
            image_parameters,
            volumes=docker_volumes
        )

    yield None
