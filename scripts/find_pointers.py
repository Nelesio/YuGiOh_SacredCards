#!/usr/bin/env python3
"""
Find all little-endian ROM pointer references to a given file offset.

Example:
    python3 find_pointers.py rom-original/SacredCards.gba 00123456
"""
import sys
import pathlib

BASE = 0x08000000  # GBA ROM mapped base

def find_pointer_locations(rom_bytes: bytes, file_off: int):
    ptr = BASE + file_off
    sig = ptr.to_bytes(4, 'little')
    return [i for i in range(0, len(rom_bytes) - 3) if rom_bytes[i:i+4] == sig]

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <rom.gba> <hex_file_offset>")
        print(f"Example: {sys.argv[0]} rom-original/SacredCards.gba 00123456")
        sys.exit(1)

    rom_path = pathlib.Path(sys.argv[1])
    file_off = int(sys.argv[2], 16)

    data = rom_path.read_bytes()
    locs = find_pointer_locations(data, file_off)
    for i in locs:
        print(f"0x{i:08X}")
    print(f"Found {len(locs)} locations.")

if __name__ == '__main__':
    main()

