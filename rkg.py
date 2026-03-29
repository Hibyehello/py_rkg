from enum import Enum
import struct
from fastcrc import crc32
import os

from .mii import Mii

"""
    A Mario Kart Wii RKG Python Library

    RKG is the file format for a Ghost
"""


class Controller_Type(Enum):
    WHEEL = 0x0
    NUNCHUCK = 0x1
    CLASSIC = 0x2
    GAMECUBE = 0x3


class Character(Enum):
    MARIO = 0x00
    BABY_PEACH = 0x01
    WALUIGI = 0x02
    BOWSER = 0x03
    BABY_DAISY = 0x04
    DRY_BONES = 0x05
    BABY_MARIO = 0x06
    LUIGI = 0x07
    TOAD = 0x08
    DONKEY_KONG = 0x09
    YOSHI = 0x0A
    WARIO = 0x0B
    BABY_LUIGI = 0x0C
    TOADETTE = 0x0D
    KOOPA_TROOPA = 0x0E
    DAISY = 0x0F
    PEACH = 0x10
    BIRDO = 0x11
    DIDDY_KONG = 0x12
    KING_BOO = 0x13
    BOWSER_JR = 0x14
    DRY_BOWSER = 0x15
    FUNKY_KONG = 0x16
    ROSALINA = 0x17
    SMALL_MII_OUTFIT_A_MALE = 0x18
    SMALL_MII_OUTFIT_A_FEMALE = 0x19
    SMALL_MII_OUTFIT_B_MALE = 0x1A
    SMALL_MII_OUTFIT_B_FEMALE = 0x1B
    SMALL_MII_OUTFIT_C_MALE = 0x1C
    SMALL_MII_OUTFIT_C_FEMALE = 0x1D
    MEDIUM_MII_OUTFIT_A_MALE = 0x1E
    MEDIUM_MII_OUTFIT_A_FEMALE = 0x1F
    MEDIUM_MII_OUTFIT_B_MALE = 0x20
    MEDIUM_MII_OUTFIT_B_FEMALE = 0x21
    MEDIUM_MII_OUTFIT_C_MALE = 0x22
    MEDIUM_MII_OUTFIT_C_FEMALE = 0x23
    LARGE_MII_OUTFIT_A_MALE = 0x24
    LARGE_MII_OUTFIT_A_FEMALE = 0x25
    LARGE_MII_OUTFIT_B_MALE = 0x26
    LARGE_MII_OUTFIT_B_FEMALE = 0x27
    LARGE_MII_OUTFIT_C_MALE = 0x28
    LARGE_MII_OUTFIT_C_FEMALE = 0x29
    MEDIUM_MII = 0x2A
    SMALL_MII = 0x2B
    LARGE_MII = 0x2C
    PEACH_MENU = 0x2D
    DAISY_MENU = 0x2E
    ROSALINA_MENU = 0x2F


class Vehicle(Enum):
    STANDARD_KART_S = 0x00
    STANDARD_KART_M = 0x01
    STANDARD_KART_L = 0x02
    BOOSTER_SEAT = 0x03
    CLASSIC_DRAGSTER = 0x04
    OFFROADER = 0x05
    MINI_BEAST = 0x06
    WILD_WING = 0x07
    FLAME_FLYER = 0x08
    CHEEP_CHARGER = 0x09
    SUPER_BLOOPER = 0x0A
    PIRANHA_PROWLER = 0x0B
    TINY_TITAN = 0x0C
    DAYTRIPPER = 0x0D
    JETSETTER = 0x0E
    BLUE_FALCON = 0x0F
    SPRINTER = 0x10
    HONEYCOUPE = 0x11
    STANDARD_BIKE_S = 0x12
    STANDARD_BIKE_M = 0x13
    STANDARD_BIKE_L = 0x14
    BULLET_BIKE = 0x15
    MACH_BIKE = 0x16
    FLAME_RUNNER = 0x17
    BIT_BIKE = 0x18
    SUGARSCOOT = 0x19
    WARIO_BIKE = 0x1A
    QUACKER = 0x1B
    ZIP_ZIP = 0x1C
    SHOOTING_STAR = 0x1D
    MAGIKRUISER = 0x1E
    SNEAKSTER = 0x1F
    SPEAR = 0x20
    JET_BUBBLE = 0x21
    DOLPHIN_DASHER = 0x22
    PHANTOM = 0x23


class Drift(Enum):
    MANUAL = 0x0
    AUTOMATIC = 0x1


class Track(Enum):
    MARIO_CIRCUIT = 0x00
    MOO_MOO_MEADOWS = 0x01
    MUSHROOM_GORGE = 0x02
    GRUMBLE_VOLCANO = 0x03
    TOADS_FACTORY = 0x04
    COCONUT_MALL = 0x05
    DK_SUMMIT = 0x06
    WARIOS_GOLD_MINE = 0x07
    LUIGI_CIRCUIT = 0x08
    DAISY_CIRCUIT = 0x09
    MOONVIEW_HIGHWAY = 0x0A
    MAPLE_TREEWAY = 0x0B
    BOWSERS_CASTLE = 0x0C
    RAINBOW_ROAD = 0x0D
    DRY_DRY_RUINS = 0x0E
    KOOPA_CAPE = 0x0F
    GCN_PEACH_BEACH = 0x10
    GCN_MARIO_CIRCUIT = 0x11
    GCN_WALUIGI_STADIUM = 0x12
    GCN_DK_MOUNTAIN = 0x13
    DS_YOSHI_FALLS = 0x14
    DS_DESERT_HILLS = 0x15
    DS_PEACH_GARDENS = 0x16
    DS_DELFINO_SQUARE = 0x17
    SNES_MARIO_CIRCUIT_3 = 0x18
    SNES_GHOST_VALLEY_2 = 0x19
    N64_MARIO_RACEWAY = 0x1A
    N64_SHERBET_LAND = 0x1B
    N64_BOWSERS_CASTLE = 0x1C
    N64_DKS_JUNGLE_PARKWAY = 0x1D
    GBA_BOWSER_CASTLE_3 = 0x1E
    GBA_SHY_GUY_BEACH = 0x1F


class Ghost(Enum):
    PLAYERS_BEST_TIME = 0x01
    WORLD_RECORD = 0x02
    CONTINENTAL_RECORD = 0x03
    RIVAL = 0x04
    SPECIAL = 0x05
    GHOST_RACE = 0x06
    FRIEND_1 = 0x07
    FRIEND_2 = 0x08
    FRIEND_3 = 0x09
    FRIEND_4 = 0x0A
    FRIEND_5 = 0x0B
    FRIEND_6 = 0x0C
    FRIEND_7 = 0x0D
    FRIEND_8 = 0x0E
    FRIEND_9 = 0x0F
    FRIEND_10 = 0x10
    FRIEND_11 = 0x11
    FRIEND_12 = 0x12
    FRIEND_13 = 0x13
    FRIEND_14 = 0x14
    FRIEND_15 = 0x15
    FRIEND_16 = 0x16
    FRIEND_17 = 0x17
    FRIEND_18 = 0x18
    FRIEND_19 = 0x19
    FRIEND_20 = 0x1A
    FRIEND_21 = 0x1B
    FRIEND_22 = 0x1C
    FRIEND_23 = 0x1D
    FRIEND_24 = 0x1E
    FRIEND_25 = 0x1F
    FRIEND_26 = 0x20
    FRIEND_27 = 0x21
    FRIEND_28 = 0x22
    FRIEND_29 = 0x23
    FRIEND_30 = 0x24
    NORMAL_STAFF = 0x25
    EXPERT_STAFF = 0x26


class Timer:
    minutes = 0
    seconds = 0
    ms_secs = 0

    def parse_bytes(self, b):
        raw = struct.unpack(">BBB", b)

        self.minutes = (raw[0] >> 1) & 0x7F
        self.seconds = (raw[0] & 0x1) << 6
        self.seconds |= (raw[1] >> 2) & 0x7F
        self.ms_secs = (raw[1] & 0x3) << 8
        self.ms_secs |= raw[2] & 0x3FF

    def pack_bytes(self):
        raw = [0] * 3

        raw[0] = (self.minutes << 1)
        raw[0] |= ((self.seconds >> 6) & 0x1)
        raw[1] = ((self.seconds & 0x3F) << 2)
        raw[1] |= ((self.ms_secs >> 8) & 0x3)
        raw[2] = self.ms_secs & 0xFF

        return bytes(raw)


class rkg_header:
    out_file = "out.rkg"
    ID = ""
    timer = Timer()
    track_id = 0
    vehicle_id = 0
    character_id = 0
    year = 0
    month = 0
    day = 0
    controller = 0
    compressed = False
    ghost_type = 0
    drift_type = 0
    data_length = 0
    lap_count = 0
    splits = [Timer() for _ in range(5)]
    country_code = 0
    state_code = 0
    location_code = 0

    mii = Mii()

    input_buffer = [0]

    def parse_file(self, file):
        """
            This Function expects an already open file so that it will read
            through the file for what it handles, and then later functions
            can continue where this function left off.
        """
        self.ID = struct.unpack(">4s", file.read(4))[0].decode("utf-8")
        self.timer.parse_bytes(file.read(3))

        self.track_id = Track(int.from_bytes(file.read(1), 'big') >> 2)

        raw = struct.unpack(">BBBB", file.read(4))

        self.vehicle_id = Vehicle(raw[0] >> 2)
        self.character_id = ((raw[0] & 0x3) << 4)
        self.character_id |= (raw[1] >> 4)
        self.character_id = Character(self.character_id)
        self.year = ((raw[1] & 0x0F) << 3)
        self.year |= (raw[2] >> 5)
        self.month = (raw[2] & 0x1E) >> 1
        self.day = ((raw[2] & 0x1) << 4)
        self.day |= (raw[3] >> 4)
        self.controller = Controller_Type(raw[3] & 0x0F)

        raw_comp_g = int.from_bytes(file.read(2), "big")
        self.compressed = bool((raw_comp_g >> 11) & 0x1)
        self.ghost_type = Ghost((raw_comp_g >> 2) & 0x7F)
        self.drift_type = Drift((raw_comp_g & 0x2) >> 1)

        self.data_length = int.from_bytes(file.read(2), "big")
        self.lap_count = int.from_bytes(file.read(1), "big")

        for i in range(len(self.splits)):
            self.splits[i].parse_bytes(file.read(3))

        file.read(0x14)

        self.country_code = int.from_bytes(file.read(1), "big")
        self.state_code = int.from_bytes(file.read(1), "big")
        self.location_code = int.from_bytes(file.read(2), "big")

        file.read(4)

        self.mii.parse_file(file)

        file.read(2)
        cur_pos = file.tell()
        file.seek(0, os.SEEK_END)
        end = file.tell()
        file.seek(cur_pos, os.SEEK_SET)
        self.input_buffer = file.read(end-cur_pos-4)

    def pack_bytes(self):
        output = bytearray()
        output += struct.pack(">4s", self.ID.encode("ascii"))
        output += self.timer.pack_bytes()
        output += bytes([self.track_id.value << 2])

        temp = [0]*4

        temp[0] = (self.vehicle_id.value << 2)
        temp[0] |= (self.character_id.value >> 4)
        temp[1] = ((self.character_id.value & 0xF) << 4)
        temp[1] |= (self.year >> 3)
        temp[2] = ((self.year & 0x7) << 5)
        temp[2] |= (self.month << 1)
        temp[2] |= (self.day >> 4)
        temp[3] = ((self.day & 0xF) << 4)
        temp[3] |= self.controller.value

        output += bytes(temp)

        temp = [0]*2

        temp[0] = (self.compressed << 3)
        temp[0] |= (self.ghost_type.value >> 7)
        temp[1] = ((self.ghost_type.value & 0x7F) << 2)
        temp[1] |= (self.drift_type.value << 1)

        output += bytes(temp)

        output += struct.pack(">H", self.data_length)
        output += bytes([self.lap_count & 0xFF])

        for split in self.splits:
            output += split.pack_bytes()

        output += bytes([0]*0x14)

        output += bytes([self.country_code & 0xFF])
        output += bytes([self.state_code & 0xFF])
        output += struct.pack(">H", self.location_code)
        output += bytes([0]*4)

        output += self.mii.pack_bytes()

        output += bytes(self.input_buffer)

        crc = crc32.iso_hdlc(bytes(output))

        print(f"CRC32 is {hex(crc)}")

        output += crc.to_bytes(4, "big")

        return output

    def __str__(self):
        s_obj = f'{self.ID}\n'
        s_obj += f'{self.timer.minutes}:{self.timer.seconds}.'
        s_obj += f'{self.timer.ms_secs}\n'
        s_obj += f'{self.track_id.name}\n'
        s_obj += f'{self.vehicle_id.name}\n'
        s_obj += f'{self.character_id.name}\n'
        s_obj += f'{self.day}/{self.month}/{self.year}\n'
        s_obj += f'{self.controller.name}\n'
        s_obj += f'{self.compressed}\n'
        s_obj += f'{self.ghost_type.name}\n'
        s_obj += f'{self.drift_type.name}\n'
        s_obj += f'{self.data_length}\n'
        s_obj += f'{self.lap_count}\n'

        for split in self.splits:
            s_obj += f'{split.minutes}:{split.seconds}.{split.ms_secs}\n'

        s_obj += f'{hex(self.country_code)}\n'
        s_obj += f'{hex(self.state_code)}\n'
        s_obj += f'{hex(self.location_code)}\n'
        s_obj += '\nMii Data:\n'
        s_obj += self.mii.__str__()

        return s_obj
