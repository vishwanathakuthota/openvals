import json
from pathlib import Path
import openvals

def dataset_root():
    return (
        Path(openvals.__file__).resolve().parent
        / "datasets"
    )

def test_dataset_command(run_cli):
    result = run_cli("datasets")
    assert result.returncode == 0, result.stderr
    assert "Available OpenVals Datasets" in result.stdout

def test_required_datasets_exist():
    for domain in (
        "finance",
        "healthcare",
        "cybersecurity",
    ):
        path = dataset_root() / domain / "dataset.json"
        assert path.is_file(), f"Missing dataset: {path}"

def test_dataset_json_valid():
    for domain in (
        "finance",
        "healthcare",
        "cybersecurity",
    ):
        path = dataset_root() / domain / "dataset.json"

        with path.open(encoding="utf-8") as file:
            data = json.load(file)

        assert isinstance(data, (list, dict))
        assert bool(data)

def test_dataset_registry_import():
    from openvals.datasets import registry
    assert registry is not None
