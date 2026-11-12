import importlib

def test_benchmark_engine_import():
    module = importlib.import_module(
        "openvals.benchmarking.benchmark"
    )
    assert module is not None

def test_benchmark_runner_import():
    module = importlib.import_module(
        "openvals.benchmarking.benchmark_runner"
    )
    assert module is not None

def test_benchmark_cli(run_cli):
    result = run_cli("benchmark", "--help")
    assert result.returncode == 0, result.stderr
    assert "Usage" in result.stdout or "usage" in result.stdout

def test_benchmark_dataset_option(run_cli):
    result = run_cli("benchmark", "--help")
    assert result.returncode == 0, result.stderr
    assert "dataset" in result.stdout.lower()
