
def test_doctor_runs(run_cli):
    result = run_cli("doctor")
    assert result.returncode == 0, result.stderr
    assert "OpenVals Doctor" in result.stdout

def test_doctor_environment(run_cli):
    result = run_cli("doctor")
    assert result.returncode == 0, result.stderr
    for field in ("Python", "Platform", "CPU Cores"):
        assert field in result.stdout

def test_system_diagnostics(run_cli):
    result = run_cli("system")
    assert result.returncode == 0, result.stderr
    assert "CPU Cores" in result.stdout
    assert "Memory GB" in result.stdout
    assert "Recommended Workers" in result.stdout

def test_gpu_diagnostics(run_cli):
    result = run_cli("system")
    assert result.returncode == 0, result.stderr
    assert "GPU / Acceleration" in result.stdout
    assert "Backend" in result.stdout
