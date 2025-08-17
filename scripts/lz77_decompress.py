#!/usr/bin/env python3
"""
Minimal GBA LZ77 (0x10) decompressor.

Example:
    python3 lz77_decompress.py rom-original/SacredCards.gba 00ABCDEF out.bin
"""
import sys
import pathlib

def lz77_decompress(data: bytes, start: int = 0) -> bytes:
    if data[start] != 0x10:
        raise ValueError("Not an 0x10 LZ77 stream")
    out_len = int.from_bytes(data[start+1:start+4], 'little')
    i = start + 4
    out = bytearray()
    while len(out) < out_len:
        flags = data[i]; i += 1
        for bit in range(8):
            if flags & (0x80 >> bit):
                b1, b2 = data[i], data[i+1]; i += 2
                count = (b1 >> 4) + 3
                disp = ((b1 & 0x0F) << 8) | b2
                pos = len(out) - (disp + 1)
                for _ in range(count):
                    out.append(out[pos]); pos += 1
            else:
                out.append(data[i]); i += 1
            if len(out) >= out_len:
                break
    return bytes(out)

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <rom.gba> <hex_offset> <out.bin>")
        sys.exit(1)

    rom_path = pathlib.Path(sys.argv[1])
    off = int(sys.argv[2], 16)
    out_path = pathlib.Path(sys.argv[3])

    rom = rom_path.read_bytes()
    blob = lz77_decompress(rom, off)
    out_path.write_bytes(blob)
    print(f"Decompressed {len(blob)} bytes → {out_path}")

if __name__ == '__main__':
    main()

