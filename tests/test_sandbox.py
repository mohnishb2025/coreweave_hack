from pathlib import Path

from repair_loop.sandbox import DockerVerifier
from repair_loop.schemas import SandboxConfig


def test_docker_command_has_isolation_and_resource_limits(tmp_path: Path) -> None:
    config = SandboxConfig(
        image="runner:test",
        command=["python", "-m", "pytest"],
        cpus=1.5,
        memory="2g",
        pids_limit=100,
    )
    command = DockerVerifier(config).docker_command(tmp_path)
    joined = " ".join(command)
    assert "--network none" in joined
    assert "--cpus 1.5" in joined
    assert "--memory 2g" in joined
    assert "--pids-limit 100" in joined
    assert "--user 65534:65534" in joined
    assert "--read-only" in command
    assert "--cap-drop ALL" in joined
    assert "no-new-privileges" in joined
    assert command[-3:] == ["python", "-m", "pytest"]


def test_mount_is_read_only(tmp_path: Path) -> None:
    command = DockerVerifier(SandboxConfig()).docker_command(tmp_path)
    mount = command[command.index("--mount") + 1]
    assert "dst=/workspace" in mount
    assert mount.endswith(",readonly")


def test_hidden_tests_are_mounted_read_only(tmp_path: Path) -> None:
    repository = tmp_path / "repo"
    hidden = tmp_path / "hidden"
    repository.mkdir()
    hidden.mkdir()

    command = DockerVerifier(SandboxConfig()).docker_command(
        repository,
        command=["python", "-m", "pytest", "-q", "/hidden_tests"],
        hidden_tests=hidden,
    )

    joined = " ".join(command)
    assert "dst=/hidden_tests,readonly" in joined
    assert "PYTHONPATH=/workspace" in joined
