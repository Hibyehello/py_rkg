import os
import pytest

from pathlib import Path

from rkg_py.mii import Mii


def test_parse_file(file_path="test.rkg"):
    script_directory = Path(__file__).parent.resolve()
    mii_data = Mii()

    with open(script_directory / file_path, "rb") as rkg_file:
        rkg_file.read(0x3C)

        mii_data.parse_file(rkg_file)

        assert mii_data.invalid == False
        assert mii_data.is_girl == False
        assert mii_data.month == 0
        assert mii_data.day == 0
        assert mii_data.fav_color == 5
        assert mii_data.is_favorite == False
        assert mii_data.name == "spock\x00\x00\x00\x00\x00"
        assert mii_data.height == 127
        assert mii_data.weight == 41
        assert mii_data.mii_id == [130, 159, 234, 94]
        assert mii_data.system_id == [48, 93, 134, 224]
        assert mii_data.face_shape == 0
        assert mii_data.skin_color == 0
        assert mii_data.facial_features == 0
        assert mii_data.mingle_off == True
        assert mii_data.downloaded == False
        assert mii_data.hair_type == 33
        assert mii_data.hair_color == 1
        assert mii_data.hair_part == 0
        assert mii_data.eyebrow_type == 4
        assert mii_data.eyebrow_rot == 10
        assert mii_data.eyebrow_color == 1
        assert mii_data.eyebrow_size == 7
        assert mii_data.eyebrow_vertical == 10
        assert mii_data.eyebrow_spacing == 12
        assert mii_data.eye_type == 2
        assert mii_data.eye_rot == 4
        assert mii_data.eye_vertical == 12
        assert mii_data.eye_color == 0
        assert mii_data.eye_size == 4
        assert mii_data.eye_spacing == 2
        assert mii_data.nose_type == 1
        assert mii_data.nose_size == 4
        assert mii_data.nose_vertical == 9
        assert mii_data.lip_type == 23
        assert mii_data.lip_color == 0
        assert mii_data.lip_size == 4
        assert mii_data.lip_vertical == 13
        assert mii_data.glasses_type == 0
        assert mii_data.glasses_color == 0
        assert mii_data.glasses_size == 4
        assert mii_data.glasses_vertical == 10
        assert mii_data.mustache_type == 0
        assert mii_data.beard_type == 0
        assert mii_data.facial_hair_color == 0
        assert mii_data.mustache_size == 4
        assert mii_data.mustache_vertical == 10
        assert mii_data.has_mole == False
        assert mii_data.mole_size == 4
        assert mii_data.mole_vertical == 20
        assert mii_data.mole_horizontal == 2
        assert mii_data.creator_name == "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


def test_pack_bytes():
    script_directory = Path(__file__).parent.resolve()

    mii_data = Mii()

    mii_data.invalid = False
    mii_data.is_girl = False
    mii_data.month = 0
    mii_data.day = 0
    mii_data.fav_color = 5
    mii_data.is_favorite = False
    mii_data.name = "spock\x00\x00\x00\x00\x00"
    mii_data.height = 127
    mii_data.weight = 41
    mii_data.mii_id = [130, 159, 234, 94]
    mii_data.system_id = [48, 93, 134, 224]
    mii_data.face_shape = 0
    mii_data.skin_color = 0
    mii_data.facial_features = 0
    mii_data.mingle_off = True
    mii_data.downloaded = False
    mii_data.hair_type = 33
    mii_data.hair_color = 1
    mii_data.hair_part = 0
    mii_data.eyebrow_type = 4
    mii_data.eyebrow_rot = 10
    mii_data.eyebrow_color = 1
    mii_data.eyebrow_size = 7
    mii_data.eyebrow_vertical = 10
    mii_data.eyebrow_spacing = 12
    mii_data.eye_type = 2
    mii_data.eye_rot = 4
    mii_data.eye_vertical = 12
    mii_data.eye_color = 0
    mii_data.eye_size = 4
    mii_data.eye_spacing = 2
    mii_data.nose_type = 1
    mii_data.nose_size = 4
    mii_data.nose_vertical = 9
    mii_data.lip_type = 23
    mii_data.lip_color = 0
    mii_data.lip_size = 4
    mii_data.lip_vertical = 13
    mii_data.glasses_type = 0
    mii_data.glasses_color = 0
    mii_data.glasses_size = 4
    mii_data.glasses_vertical = 10
    mii_data.mustache_type = 0
    mii_data.beard_type = 0
    mii_data.facial_hair_color = 0
    mii_data.mustache_size = 4
    mii_data.mustache_vertical = 10
    mii_data.has_mole = False
    mii_data.mole_size = 4
    mii_data.mole_vertical = 20
    mii_data.mole_horizontal = 2
    mii_data.creator_name = "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    with open(script_directory / "out_mii.rkg", "wb") as out:
        out.write(b"\x00" * 0x3C)
        out.write(mii_data.pack_bytes())

    test_parse_file("out_mii.rkg")

    os.remove(script_directory / "out_mii.rkg")

