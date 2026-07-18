from __future__ import annotations

from {{PACKAGE_NAME}} import __version__
from {{PACKAGE_NAME}}.cli import main


def test_version_output(capsys: object) -> None:
    assert main(["--version"]) == 0
    captured = capsys.readouterr()  # type: ignore[attr-defined]
    assert captured.out.strip() == __version__
