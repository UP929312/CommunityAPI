from base64 import b64decode
from gzip import decompress
from io import BytesIO
from struct import unpack

from typing import Union

def parse_container(raw: str) -> list:
    """
    This will decompress and decode the base64 data that Hypixel returns from the API.
    This will then get parsed into one of the other functions below
    """
    raw_bytes = BytesIO(decompress(b64decode(raw)))   # Unzip raw string from the api

    def read(type, length):
        if type in 'chil':
            return int.from_bytes(raw_bytes.read(length), byteorder='big')
        if type == 's':
            return raw_bytes.read(length).decode('utf-8')
        return unpack('>' + type, raw_bytes.read(length))[0]

    def parse_list():
        subtype = read('c', 1)
        payload = []
        for _ in range(read('i', 4)):
            parse_next_tag(payload, subtype)
        return payload

    def parse_compound():
        payload = {}
        while parse_next_tag(payload) != 0:  # Parse tags until we find an endcap (type == 0)
            pass  # Nothing needs to happen here
        return payload

    payloads = {
        1: lambda: read('c', 1),  # Byte
        2: lambda: read('h', 2),  # Short
        3: lambda: read('i', 4),  # Int
        4: lambda: read('l', 8),  # Long
        5: lambda: read('f', 4),  # Float
        6: lambda: read('d', 8),  # Double
        7: lambda: raw_bytes.read(read('i', 4)),  # Byte Array
        8: lambda: read('s', read('h', 2)),  # String
        9: parse_list,  # List
        10: parse_compound,  # Compound
        11: lambda: [read('i', 4) for _ in range(read('i', 4))],  # Int Array
        12: lambda: [read('l', 8) for _ in range(read('i', 4))]  # Long Array
    }

    def parse_next_tag(dictionary, tag_id=None):
        if tag_id is None:  # Are we inside a list?
            tag_id = read('c', 1)
            if tag_id == 0:  # Is this the end of a compound?
                return 0
            name = read('s', read('h', 2))

        payload = payloads[tag_id]()
        if isinstance(dictionary, dict):
            dictionary[name] = payload
        else:
            dictionary.append(payload)

    raw_bytes.read(3)  # Remove file header (we ingore footer)
    root: dict = {}
    parse_next_tag(root)
    if not root:
        return []
    return [x for x in root['i'] if x]

def extract_internal_id(nbt: dict) -> str:
    """
    Takes the data from the decode container function and returns
    the internal_id
    """
    tag = nbt.get('tag', {})
    internal_name = tag.get('ExtraAttributes', {"id": "UNKNOWN"}).get('id', "UNKNOWN")

    return internal_name

def extract_nbt_dicts(raw: str) -> list[dict]:
    """
    Takes a raw compressed encoded string and returns all the items in that
    list in an nbt dictionary
    """
    return [x['tag'] for x in parse_container(raw) if 'tag' in x.keys()]

def extract_internal_names(raw: str) -> list[str]:
    """
    Extracts all the internal names from a container
    """
    return [extract_internal_id(x) for x in parse_container(raw)]


