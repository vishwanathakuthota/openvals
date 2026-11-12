
def test_provider_command(run_cli):
    result = run_cli("providers")
    assert result.returncode == 0, result.stderr
    assert "OpenVals Provider Intelligence" in result.stdout

def test_provider_status_fields(run_cli):
    result = run_cli("providers")

    assert result.returncode == 0, result.stderr

    for field in (
        "Configured",
        "Reachable",
        "Authenticated",
        "Benchmark Ready",
    ):
        assert field in result.stdout

def test_provider_names(run_cli):
    result = run_cli("providers")

    assert result.returncode == 0, result.stderr

    output = result.stdout.lower()

    for provider in (
        "ollama",
        "openai",
        "anthropic",
        "gemini",
    ):
        assert provider in output
