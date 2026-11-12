import importlib

def test_models_command(run_cli):
    result = run_cli("models")
    assert result.returncode == 0, result.stderr
    assert "OpenVals Model Catalog" in result.stdout

def test_model_catalog_columns(run_cli):
    result = run_cli("models")
    assert result.returncode == 0, result.stderr
    for column in ("Model", "Provider", "Type"):
        assert column in result.stdout

def test_model_discovery_import():
    module = importlib.import_module(
        "openvals.models.discovery"
    )

    assert module is not None

def test_model_registry_import():
    module = importlib.import_module(
        "openvals.models.registry"
    )

    assert module is not None
