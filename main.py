#!/usr/bin/env python3
"""Write the rogue-agent meme to /output/entry.png.

The artwork is stored as artwork.png next to this file and is copied byte
for byte, so the output is deterministic. Python 3 standard library only;
no network access, no randomness.
"""
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_DIM = 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "artwork.png")
    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("artwork.png is not a PNG file")
    if data[12:16] != b"IHDR":
        sys.exit("artwork.png has no IHDR chunk")
    if len(data) > MAX_BYTES:
        sys.exit("artwork.png exceeds the 1 MiB limit")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        sys.exit("artwork.png exceeds the 1024x1024 limit")
    os.makedirs("/output", exist_ok=True)
    out = "/output/entry.png"
    with open(out, "wb") as f:
        f.write(data)
    with open(out, "rb") as f:
        if f.read() != data:
            sys.exit("output does not match artwork.png")
    print("wrote /output/entry.png (%d bytes, %dx%d)"
          % (len(data), width, height))


if __name__ == "__main__":
    main()
