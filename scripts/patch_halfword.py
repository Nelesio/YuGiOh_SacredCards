#!/usr/bin/env python3
"""
Patch a 16-bit little-endian value at a ROM file offset.

Examples:
    python3 patch_halfword.py rom-original/SacredCards.gba 0012ABCD 300
    python3 patch_halfword.py rom-original/SacredCards.gba 0012ABCD 0x012C
"""
import sys
import pathlib

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <rom.gba> <hex_offset> <new_value_dec_or_hex>")
        sys.exit(1)

    rom_path = pathlib.Path(sys.argv[1])
    off = int(sys.argv[2], 16)
    val = int(sys.argv[3], 0)  # accepts decimal or 0x-prefixed hex

    data = bytearray(rom_path.read_bytes())
    if off < 0 or off + 2 > len(data):
        print("Error: offset out of range")
        sys.exit(2)

    data[off:off+2] = val.to_bytes(2, 'little')

    out_dir = rom_path.parent.parent / 'rom-hacked'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (rom_path.stem + f"_hw_{val}" + rom_path.suffix)
    out_path.write_bytes(data)

    print(f"Wrote 0x{val:04X} at 0x{off:08X}")
    print(f"→ {out_path}")

if __name__ == '__main__':
    main()

