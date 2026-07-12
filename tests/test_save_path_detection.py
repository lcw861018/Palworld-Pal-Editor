import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from palworld_pal_editor.utils.util import resolve_pal_save_path
from palworld_pal_editor.core.save_manager import MAIN_SKIP_PROPERTIES, SaveManager


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


def test_main_skip_properties_skip_group_save_data_map():
    assert ".worldSaveData.GroupSaveDataMap" in MAIN_SKIP_PROPERTIES


def test_load_entities_creates_player_without_group_id(monkeypatch):
    manager = SaveManager()
    manager.player_mapping = {}
    manager._dangling_pals = {}
    manager.baseworker_mapping = {}
    manager.group_data = None
    manager.container_data = None
    manager._entities_list = [
        {
            "key": {
                "PlayerUId": {"value": "11111111-1111-1111-1111-111111111111"},
                "InstanceId": {"value": "22222222-2222-2222-2222-222222222222"},
            },
            "value": {
                "RawData": {
                    "value": {
                        "object": {
                            "SaveParameter": {
                                "struct_type": "PalIndividualCharacterSaveParameter",
                                "value": {
                                    "IsPlayer": {"value": True},
                                    "NickName": {"value": "Tester"},
                                },
                            }
                        }
                    }
                }
            },
        }
    ]

    class DummyGvasFile:
        properties = {
            "SaveData": {
                "value": {
                    "IndividualId": {
                        "value": {
                            "PlayerUId": {"value": "11111111-1111-1111-1111-111111111111"},
                            "InstanceId": {"value": "22222222-2222-2222-2222-222222222222"},
                        }
                    }
                }
            }
        }

    monkeypatch.setattr(manager, "load_player_sav", lambda uid: (DummyGvasFile(), 0))

    manager._load_entities()

    assert "11111111-1111-1111-1111-111111111111" in manager.player_mapping
