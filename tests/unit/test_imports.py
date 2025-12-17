"""
Test that the package can be imported correctly.
"""

import pytest


def test_import_dndsheet():
    """Test that the main package can be imported."""
    import dndsheet

    assert dndsheet is not None


def test_package_version():
    """Test that the package has a version."""
    import dndsheet

    assert hasattr(dndsheet, "__version__")
    assert isinstance(dndsheet.__version__, str)
    assert len(dndsheet.__version__) > 0


def test_import_cli():
    """Test that the CLI module can be imported."""
    from dndsheet import cli

    assert cli is not None
    assert hasattr(cli, "main")
    assert callable(cli.main)
