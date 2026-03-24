"""Word 测试共享 fixture。"""

import struct
import zlib

import pytest


@pytest.fixture
def minimal_png() -> bytes:
    """创建最小 PNG 图片数据。"""

    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        c = chunk_type + data
        return (
            struct.pack(">I", len(data))
            + c
            + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        )

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 8, 2, 0, 0, 0))
    raw = b""
    for _ in range(2):
        raw += b"\x00"
        for _ in range(2):
            raw += b"\xff\x00\x00"
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend
