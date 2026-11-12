import importlib.metadata
from openvals import __version__

def test_version_is_defined():
    assert isinstance(__version__, str)
    assert __version__.strip()

def test_version_matches_package_metadata():
    installed_version = importlib.metadata.version("openvals")

    assert __version__ == installed_version