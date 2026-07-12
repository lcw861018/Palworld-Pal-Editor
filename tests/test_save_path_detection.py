import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from palworld_pal_editor.utils.util import resolve_pal_save_path


def test_resolve_pal_save_path_finds_descendant_save_dir(tmp_path):
    save_dir = tmp_path / "SaveGames" / "0" / "abc123"
    (save_dir / "Players").mkdir(parents=True)
    (save_dir / "Level.sav").write_bytes(b"test")

    resolved = resolve_pal_save_path(tmp_path / "SaveGames")

    assert resolved == save_dir


def test_resolve_pal_save_path_returns_existing_save_dir(tmp_path):
    save_dir = tmp_path / "SaveGames" / "0" / "abc123"
    (save_dir / "Players").mkdir(parents=True)
    (save_dir / "Level.sav").write_bytes(b"test")

    resolved = resolve_pal_save_path(save_dir)

    assert resolved == save_dir
