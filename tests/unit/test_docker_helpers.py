from deeptracy_core.docker_helpers import run_in_docker

import tempfile


def test_run_in_docker_ok():
    CMD = """sh -c "echo hello > /tmp/$OUTPUT_FILE" """

    with tempfile.TemporaryDirectory(dir="/tmp") as source:
        with run_in_docker(
                "busybox",
                source_code_path=source,
                result_path="/tmp",
                command=CMD) as f:
            assert f == "hello\n"
