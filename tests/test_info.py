"""Tests for CLI presentation helpers."""

from io import StringIO

from rich.console import Console

from openloci import cli


def test_info_uses_plain_text_and_truncates_by_line(monkeypatch, tmp_path):
    vestibule = tmp_path / "the-vestibule"
    vestibule.mkdir()
    lines = ["[bold]literal[/bold]"] + [f"line-{index:02d} {'x' * 40}" for index in range(1, 45)]
    (vestibule / "README.md").write_text("\n".join(lines))
    output = StringIO()
    monkeypatch.setattr(cli, "console", Console(file=output, width=200, color_system=None))

    cli.info(tmp_path)

    rendered = output.getvalue()
    assert "[bold]literal[/bold]" in rendered
    assert "line-39" in rendered
    assert "line-40" not in rendered
    assert "…" in rendered
