#!/usr/bin/env python3

""" This library provides functions to encode and decode an
unsigned integer using the unsigned-varint encoding.

See also: https://github.com/multiformats/unsigned-varint
"""

def encode(num: int) -> bytes:
    """ Encode an unsigned integer using unsigned-varint encoding """

    result = b"" if num else bytes(1)

    while num:
        byte = num & 0x7f
        num = num >> 7

        if num:
            byte = byte | 0x80

        result += bytes([byte])

    return result

def decode(buffer: bytes) -> int:
    """ Decodes an unsigned-varint-encoded unsigned integer """

    result = 0

    for iteration, byte in enumerate(buffer):
        result |= (byte & 0x7f) << (iteration * 7)

        if not byte & 0x80:
            break

    return result

def test():
    """ Run some tests from https://github.com/multiformats/unsigned-varint:

    1     => 00000001
    127   => 01111111
    128   => 10000000 00000001
    255   => 11111111 00000001
    300   => 10101100 00000010
    16384 => 10000000 10000000 00000001
    """

    def dump(bytearr: bytes) -> str:
        """ Dumps a bytes object as groups of eight bit.

        >>> dump(b"\x80\x01")
        '10000000 00000001'
        """

        return ' '.join(format(byte, "08b") for byte in bytearr)

    def undump(bits: str) -> bytes:
        """ Reverses dump() - "decodes" a bitstring into bytes.

        >>> undump("10000000 00000001")
        b'\x80\x01'
        """

        return bytes([int(c, 2) for c in bits.split(" ")])

    cases = [
        [1, "00000001"],
        [127, "01111111"],
        [128, "10000000 00000001"],
        [255, "11111111 00000001"],
        [300, "10101100 00000010"],
        [16384, "10000000 10000000 00000001"]
    ]

    for case in cases:
        assert dump(encode(case[0])) == case[1]
        assert decode(undump(case[1])) == case[0]

if __name__ == "__main__":
    test()
