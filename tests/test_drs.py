import importlib

def test_drs_module_import():
    module = importlib.import_module(
        "openvals.scoring.drs"
    )
    assert module is not None

def test_weighted_scoring_import():
    module = importlib.import_module(
        "openvals.scoring.weighted"
    )
    assert module is not None

def test_normalization_import():
    module = importlib.import_module(
        "openvals.benchmarking.normalization"
    )
    assert module is not None
