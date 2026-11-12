import os
import shutil
import subprocess
import pytest

@pytest.fixture(scope="session")
def run_cli():
    """Execute the installed OpenVals CLI."""

    def execute(*args, timeout=120):
        executable = shutil.which("openvals")

        if executable is None:
            pytest.fail(
                "OpenVals CLI not installed. "
                "Run: python3 -m pip install -e ."
            )

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        return subprocess.run(
            [executable, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )

    return execute
