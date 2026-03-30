import os
import pytest

from pathlib import Path

from py_rkg.rkg import rkg_header, Track, Vehicle, Character, Controller_Type, Ghost, Drift


def test_parse_file(file_path="test.rkg"):
    script_directory = Path(__file__).parent.resolve()
    rkg_metadata = rkg_header()

    with open(script_directory / file_path, "rb") as rkg_file:
        rkg_metadata.parse_file(rkg_file)

        assert rkg_metadata.ID == "RKGD"
        assert rkg_metadata.timer.minutes == 1
        assert rkg_metadata.timer.seconds == 58
        assert rkg_metadata.timer.ms_secs == 310
        assert rkg_metadata.track_id == Track.GCN_MARIO_CIRCUIT
        assert rkg_metadata.vehicle_id == Vehicle.FLAME_RUNNER
        assert rkg_metadata.character_id == Character.FUNKY_KONG
        assert rkg_metadata.year == 26
        assert rkg_metadata.month == 3
        assert rkg_metadata.day == 8
        assert rkg_metadata.controller == Controller_Type.GAMECUBE
        assert rkg_metadata.compressed == True
        assert rkg_metadata.ghost_type == Ghost.EXPERT_STAFF
        assert rkg_metadata.drift_type == Drift.MANUAL
        assert rkg_metadata.data_length == 1078
        assert rkg_metadata.lap_count == 3
        assert rkg_metadata.splits[0].minutes == 0
        assert rkg_metadata.splits[0].seconds == 39
        assert rkg_metadata.splits[0].ms_secs == 210
        assert rkg_metadata.splits[1].minutes == 0
        assert rkg_metadata.splits[1].seconds == 40
        assert rkg_metadata.splits[1].ms_secs == 366
        assert rkg_metadata.splits[2].minutes == 0
        assert rkg_metadata.splits[2].seconds == 38
        assert rkg_metadata.splits[2].ms_secs == 734
        assert rkg_metadata.country_code == 0xFF
        assert rkg_metadata.state_code == 0xFF
        assert rkg_metadata.location_code == 0xFFFF


def test_pack_bytes():
    script_directory = Path(__file__).parent.resolve()

    rkg_metadata = rkg_header()

    rkg_metadata.ID = "RKGD"
    rkg_metadata.timer.minutes = 1
    rkg_metadata.timer.seconds = 58
    rkg_metadata.timer.ms_secs = 310
    rkg_metadata.track_id = Track.GCN_MARIO_CIRCUIT
    rkg_metadata.vehicle_id = Vehicle.FLAME_RUNNER
    rkg_metadata.character_id = Character.FUNKY_KONG
    rkg_metadata.year = 26
    rkg_metadata.month = 3
    rkg_metadata.day = 8
    rkg_metadata.controller = Controller_Type.GAMECUBE
    rkg_metadata.compressed = True
    rkg_metadata.ghost_type = Ghost.EXPERT_STAFF
    rkg_metadata.drift_type = Drift.MANUAL
    rkg_metadata.data_length = 1078
    rkg_metadata.lap_count = 3
    rkg_metadata.splits[0].minutes = 0
    rkg_metadata.splits[0].seconds = 39
    rkg_metadata.splits[0].ms_secs = 210
    rkg_metadata.splits[1].minutes = 0
    rkg_metadata.splits[1].seconds = 40
    rkg_metadata.splits[1].ms_secs = 366
    rkg_metadata.splits[2].minutes = 0
    rkg_metadata.splits[2].seconds = 38
    rkg_metadata.splits[2].ms_secs = 734
    rkg_metadata.country_code = 0xFF
    rkg_metadata.state_code = 0xFF
    rkg_metadata.location_code = 0xFFFF

    with open(script_directory / "out_test.rkg", "wb") as out:
        out.write(rkg_metadata.pack_bytes())

    test_parse_file("out_test.rkg")

    os.remove(script_directory / "out_test.rkg")


if __name__ == "__main__":
    pytest.main()
