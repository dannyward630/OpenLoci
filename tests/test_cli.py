"""Tests for CLI error handling."""

import pytest
import typer

from openloci import cli


def test_new_preserves_file_not_found_cause(monkeypatch, tmp_path):
    original_error = FileNotFoundError("skin missing")

    def fail_generate(**kwargs):
        raise original_error

    monkeypatch.setattr(cli, "generate_palace", fail_generate)

    with pytest.raises(typer.Exit) as exit_info:
        cli.new("example", output_dir=tmp_path, no_input=True)

    assert exit_info.value.__cause__ is original_error


def test_new_preserves_unexpected_error_cause(monkeypatch, tmp_path):
    original_error = RuntimeError("generation failed")

    def fail_generate(**kwargs):
        raise original_error

    monkeypatch.setattr(cli, "generate_palace", fail_generate)

    with pytest.raises(typer.Exit) as exit_info:
        cli.new("example", output_dir=tmp_path, no_input=True)

    assert exit_info.value.__cause__ is original_error


def test_rooms_preserves_missing_skin_cause(monkeypatch):
    original_error = FileNotFoundError("skin missing")

    def fail_get_skin_info(skin):
        raise original_error

    monkeypatch.setattr(cli, "get_skin_info", fail_get_skin_info)

    with pytest.raises(typer.Exit) as exit_info:
        cli.rooms("missing")

    assert exit_info.value.__cause__ is original_error
