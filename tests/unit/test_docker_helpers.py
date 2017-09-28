from deeptracy_core.docker_helpers import run_in_docker


def test_run_in_docker_ok():
    CMD = """sh -c "echo hello > $OUTPUT_FILE" """
    with run_in_docker(
            "busybox",
            working_dir="/tmp",
            command=CMD) as f:
        assert f == "hello\n"
