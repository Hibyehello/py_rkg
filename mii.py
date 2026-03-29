import struct
from fastcrc import crc16

import requests # for fetching the mii image

class Mii:
    invalid = False
    is_girl = False
    month = 0
    day = 0
    fav_color = 0
    is_favorite = False
    name = ""
    height = 0
    weight = 0

    mii_id = [0] * 4
    system_id = [0] * 4

    face_shape = 0
    skin_color = 0
    facial_features = 0
    mingle_off = False
    downloaded = False

    hair_type = 0
    hair_color = 0
    hair_part = 0

    eyebrow_type = 0
    eyebrow_rot = 0
    eyebrow_color = 0
    eyebrow_size = 0
    eyebrow_vertical = 0
    eyebrow_spacing = 0

    eye_type = 0
    eye_rot = 0
    eye_vertical = 0
    eye_color = 0
    eye_size = 0
    eye_spacing = 0

    nose_type = 0
    nose_size = 0
    nose_vertical = 0

    lip_type = 0
    lip_color = 0
    lip_size = 0
    lip_vertical = 0

    glasses_type = 0
    glasses_color = 0
    glasses_size = 0
    glasses_vertical = 0

    mustache_type = 0
    beard_type = 0
    facial_hair_color = 0
    mustache_size = 0
    mustache_vertical = 0

    has_mole = False
    mole_size = 0
    mole_vertical = 0
    mole_horizontal = 0

    creator_name = ""

    mii_crc = 0

    def parse_file(self, file):
        raw = struct.unpack(">BB", file.read(2))

        self.invalid = bool(raw[0] >> 7)
        self.is_girl = bool((raw[0] >> 6) & 0x1)
        self.month = (raw[0] >> 2) & 0xF
        self.day = ((raw[0] & 0x3) << 3) | (raw[1] >> 5)
        self.fav_color = raw[1] >> 1 & 0xF
        self.is_favorite = bool(raw[1] & 0x1)

        raw = struct.unpack(">20s", file.read(20))[0]

        self.name = raw.decode("utf-16-be")

        self.height = int(struct.unpack(">B", file.read(1))[0])
        self.weight = int(struct.unpack(">B", file.read(1))[0])

        raw = struct.unpack(">BBBB", file.read(4))

        self.mii_id = list(raw)

        raw = struct.unpack(">BBBB", file.read(4))

        self.system_id = list(raw)

        raw = struct.unpack(">BB", file.read(2))
        self.face_shape = (raw[0] >> 5)
        self.skin_color = (raw[0] >> 2) & 0x7
        self.facial_features = (raw[0] & 0x3) | (raw[1] >> 6)
        self.mingle_off = bool((raw[1] >> 2) & 0x1)
        self.downloaded = bool(raw[1] & 0x1)

        # Hair
        raw = struct.unpack(">BB", file.read(2))
        self.hair_type = raw[0] >> 1
        self.hair_color = ((raw[0] & 0x1) << 2) | (raw[1] >> 6)
        self.hair_part = ((raw[1] >> 5) & 0x1)

        # Eyebrows
        raw = struct.unpack(">BBBB", file.read(4))
        self.eyebrow_type = (raw[0] >> 3)
        self.eyebrow_rot = ((raw[0] & 0x3) << 2) | (raw[1] >> 6)
        self.eyebrow_color = (raw[2] >> 5)
        self.eyebrow_size = (raw[2] >> 1) & 0xF
        self.eyebrow_vertical = ((raw[2] & 0x1) << 4) | (raw[3] >> 4)
        self.eyebrow_spacing = (raw[3] & 0xF)

        # Eyes
        raw = struct.unpack(">BBBB", file.read(4))
        self.eye_type = (raw[0] >> 2)
        self.eye_rot = (raw[1] >> 5)
        self.eye_vertical = (raw[1] & 0x1F)
        self.eye_color = (raw[2] >> 5)
        self.eye_size = (raw[2] >> 1) & 0x7
        self.eye_spacing = (raw[2] & 0x1) | (raw[3] >> 5)

        # Nose
        raw = struct.unpack(">BB", file.read(2))
        self.nose_type = (raw[0] >> 4)
        self.nose_size = (raw[0] & 0xF)
        self.nose_vertical = (raw[1] >> 3)

        # Lips
        raw = struct.unpack(">BB", file.read(2))
        self.lip_type = (raw[0] >> 3)
        self.lip_color = (raw[0] >> 1) & 0x3
        self.lip_size = ((raw[0] & 0x1) << 3) | (raw[1] >> 5)
        self.lip_vertical = (raw[1] & 0x1F)

        # Glasses
        raw = struct.unpack(">BB", file.read(2))
        self.glasses_type = (raw[0] >> 4)
        self.glasses_color = (raw[0] >> 1) & 0x7
        self.glasses_size = (raw[1] >> 5)
        self.glasses_vertical = (raw[1] & 0x1F)

        # Facial Hair
        raw = struct.unpack(">BB", file.read(2))
        self.mustache_type = (raw[0] >> 6)
        self.beard_type = (raw[0] >> 4) & 0x3
        self.facial_hair_color = (raw[0] >> 1) & 0x7
        self.mustache_size = ((raw[0] & 0x1) << 3) | (raw[1] >> 5)
        self.mustache_vertical = (raw[1] & 0x1F)

        # Mole
        raw = struct.unpack(">BB", file.read(2))
        self.has_mole = bool(raw[0] >> 7)
        self.mole_size = (raw[0] >> 3) & 0xF
        self.mole_vertical = ((raw[0] & 0x7) << 2) | (raw[1] >> 6)
        self.mole_horizontal = (raw[1] >> 1) & 0x1F

        raw = struct.unpack(">20s", file.read(20))[0]

        self.creator_name = raw.decode("utf-16-be")

    def pack_bytes(self):
        output = bytearray()

        temp = [0] * 2

        temp[0] = int(self.invalid) << 7
        temp[0] |= int(self.is_girl) << 6
        temp[0] |= self.month << 2
        temp[0] |= self.day >> 3
        temp[1] = (self.day & 0x7) << 5
        temp[1] |= self.fav_color << 1
        temp[1] |= int(self.is_favorite)

        output += bytes(temp)

        temp = bytearray(20)
        encoded = self.name.encode("utf-16-be")
        temp[:len(encoded)] = encoded

        output += temp

        output += (self.height & 0xFF).to_bytes(1, "big")
        output += (self.weight & 0xFF).to_bytes(1, "big")

        output += bytes(self.mii_id)
        output += bytes(self.system_id)

        temp = [0] * 2

        temp[0] = (self.face_shape & 0x7) << 5
        temp[0] |= (self.skin_color & 0x7) << 2
        temp[0] |= (self.facial_features >> 2)
        temp[1] = (self.facial_features & 0x3) << 6
        temp[1] |= (self.mingle_off << 2)
        temp[1] |= self.downloaded

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = (self.hair_type & 0x7F) << 1
        temp[0] |= self.hair_color >> 2
        temp[1] = (self.hair_color & 0x3) << 6
        temp[1] |= (self.hair_part << 5)

        output += bytes(temp)

        temp = [0] * 4

        temp[0] = (self.eyebrow_type & 0x1F) << 3
        temp[0] |= (self.eyebrow_rot & 0xC) >> 2
        temp[1] = (self.eyebrow_rot & 0x3) << 6
        temp[2] = (self.eyebrow_color & 0x7) << 5
        temp[2] |= (self.eyebrow_size & 0xF) << 1
        temp[2] |= (self.eyebrow_vertical & 0x10) >> 4
        temp[3] = (self.eyebrow_vertical & 0xF) << 4
        temp[3] |= (self.eyebrow_spacing & 0xF)

        output += bytes(temp)

        temp = [0] * 4

        temp[0] = (self.eye_type & 0x3F) << 2
        temp[1] = (self.eye_rot & 0x7) << 5
        temp[1] |= (self.eye_vertical & 0x1F)
        temp[2] = (self.eye_color & 0x7) << 5
        temp[2] |= (self.eye_size & 0x7) << 1
        temp[2] |= (self.eye_spacing >> 3) & 0x1
        temp[3] = (self.eye_spacing & 0x7) << 5

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = (self.nose_type & 0xF) << 4
        temp[0] |= self.nose_size & 0xF
        temp[1] = (self.nose_vertical & 0x1F) << 3

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = (self.lip_type & 0x1F) << 3
        temp[0] |= (self.lip_color & 0x3) << 1
        temp[0] |= (self.lip_size >> 3) & 0x1
        temp[1] = (self.lip_size & 0x7) << 5
        temp[1] |= self.lip_vertical & 0x1F

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = (self.glasses_type & 0xF) << 4
        temp[0] |= (self.glasses_color & 0x7) << 1
        temp[1] = (self.glasses_size & 0x7) << 5
        temp[1] |= (self.glasses_vertical & 0x1F)

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = (self.mustache_type & 0x3) << 6
        temp[0] |= (self.beard_type & 0x3) << 4
        temp[0] |= (self.facial_hair_color & 0x7) << 1
        temp[0] |= (self.mustache_size >> 3) & 0x1
        temp[1] = (self.mustache_size & 0x7) << 5
        temp[1] |= (self.mustache_vertical & 0x1F)

        output += bytes(temp)

        temp = [0] * 2

        temp[0] = self.has_mole << 7
        temp[0] |= (self.mole_size & 0xF) << 3
        temp[0] |= (self.mole_vertical >> 2) & 0x7
        temp[1] = (self.mole_vertical & 0x3) << 6
        temp[1] |= (self.mole_horizontal & 0x1F) << 1

        output += bytes(temp)

        temp = bytearray(20)
        encoded = self.creator_name.encode("utf-16-be")
        temp[:len(encoded)] = encoded

        output += temp

        self.mii_crc = crc16.xmodem(bytes(output))

        print(f"Mii CRC16-XModem is {hex(self.mii_crc)}")

        output += self.mii_crc.to_bytes(2, "big")

        return output

    def fetch_mii_image(self):
        mii_data = self.pack_bytes()

        resp = requests.get(
                "https://mii-unsecure.ariankordi.net/miis/image.png",
                params={
                    "data": bytes(mii_data).hex(),
                    "width": 256,
                    "shaderType": "miitomo"
                    }
                )

        resp.raise_for_status()
        return resp.content

    def __str__(self):
        s_obj = f'{self.invalid}\n'
        s_obj += f'{self.is_girl}\n'
        s_obj += f'{self.month}\n'
        s_obj += f'{self.day}\n'
        s_obj += f'{self.fav_color}\n'
        s_obj += f'{self.is_favorite}\n'
        s_obj += f'{self.name}\n'
        s_obj += f'{self.height}\n'
        s_obj += f'{self.weight}\n'
        s_obj += f'{self.mii_id}\n'
        s_obj += f'{self.system_id}\n'
        s_obj += f'{self.face_shape}\n'
        s_obj += f'{self.skin_color}\n'
        s_obj += f'{self.facial_features}\n'
        s_obj += f'{self.mingle_off}\n'
        s_obj += f'{self.downloaded}\n'
        s_obj += 'Hair:\n'
        s_obj += f'{self.hair_type}\n'
        s_obj += f'{self.hair_color}\n'
        s_obj += f'{self.hair_part}\n'
        s_obj += 'Eyebrows:\n'
        s_obj += f'{self.eyebrow_type}\n'
        s_obj += f'{self.eyebrow_rot}\n'
        s_obj += f'{self.eyebrow_color}\n'
        s_obj += f'{self.eyebrow_size}\n'
        s_obj += f'{self.eyebrow_vertical}\n'
        s_obj += f'{self.eyebrow_spacing}\n'
        s_obj += 'Eyes:\n'
        s_obj += f'{self.eye_type}\n'
        s_obj += f'{self.eye_rot}\n'
        s_obj += f'{self.eye_vertical}\n'
        s_obj += f'{self.eye_color}\n'
        s_obj += f'{self.eye_size}\n'
        s_obj += f'{self.eye_spacing}\n'
        s_obj += 'Nose:\n'
        s_obj += f'{self.nose_type}\n'
        s_obj += f'{self.nose_size}\n'
        s_obj += f'{self.nose_vertical}\n'
        s_obj += 'Lips:\n'
        s_obj += f'{self.lip_type}\n'
        s_obj += f'{self.lip_color}\n'
        s_obj += f'{self.lip_size}\n'
        s_obj += f'{self.lip_vertical}\n'
        s_obj += 'Glasses:\n'
        s_obj += f'{self.glasses_type}\n'
        s_obj += f'{self.glasses_color}\n'
        s_obj += f'{self.glasses_size}\n'
        s_obj += f'{self.glasses_vertical}\n'
        s_obj += 'Facial Hair:\n'
        s_obj += f'{self.mustache_type}\n'
        s_obj += f'{self.beard_type}\n'
        s_obj += f'{self.facial_hair_color}\n'
        s_obj += f'{self.mustache_size}\n'
        s_obj += f'{self.mustache_vertical}\n'
        s_obj += 'Mole:\n'
        s_obj += f'{self.has_mole}\n'
        s_obj += f'{self.mole_size}\n'
        s_obj += f'{self.mole_vertical}\n'
        s_obj += f'{self.mole_horizontal}\n'
        s_obj += f'{self.creator_name}'

        return s_obj
