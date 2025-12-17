"""
Test the CLI functionality.
"""

import pytest
import subprocess
import sys
from pathlib import Path


def test_cli_help():
    """Test that the CLI help command works."""
    result = subprocess.run(
        [sys.executable, "-m", "dndsheet", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "D&D Character Sheet Generator" in result.stdout


def test_cli_version():
    """Test that the CLI version command works."""
    result = subprocess.run(
        [sys.executable, "-m", "dndsheet", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "dndsheet" in result.stdout
    assert "0.1.0" in result.stdout


def test_cli_no_args():
    """Test that running CLI with no args shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "dndsheet"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()


def test_cli_check_command():
    """Test that the check command exists (even if not implemented)."""
    result = subprocess.run(
        [sys.executable, "-m", "dndsheet", "check"],
        capture_output=True,
        text=True,
    )
    # Should run without crashing (may return 1 as not implemented)
    assert result.returncode in [0, 1]


def test_cli_generate_command_placeholder():
    """Test that the generate command exists (placeholder)."""
    result = subprocess.run(
        [sys.executable, "-m", "dndsheet", "generate", "nonexistent.json"],
        capture_output=True,
        text=True,
    )
    # Should run without crashing (returns 1 as not implemented)
    assert result.returncode == 1
    assert "not yet implemented" in result.stdout.lower()
