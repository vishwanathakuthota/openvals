import importlib

def test_trust_readiness_import():
    module = importlib.import_module(
        "openvals.advisor.trust_readiness"
    )
    assert module is not None

def test_trust_verdict_import():
    module = importlib.import_module(
        "openvals.advisor.trust_verdict"
    )
    assert module is not None

def test_trust_advisor_cli(run_cli):
    result = run_cli("trust-advisor", "--help")
    assert result.returncode == 0, result.stderr
    assert "Usage" in result.stdout or "usage" in result.stdout
