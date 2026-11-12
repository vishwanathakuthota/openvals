import importlib
def test_recommendation_engine_import():
    module = importlib.import_module(
        "openvals.advisor.recommendation_engine"
    )
    assert module is not None

def test_model_catalog_import():
    module = importlib.import_module(
        "openvals.advisor.model_catalog"
    )
    assert module is not None

def test_recommendation_cli(run_cli):
    result = run_cli("recommend-model", "--help")

    assert result.returncode == 0, result.stderr
    assert "Usage" in result.stdout or "usage" in result.stdout
