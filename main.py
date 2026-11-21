#!/usr/bin/env python3
"""news-image-20261121 entry: deliver the finished front page.

The image itself was drawn outside this repo (build_news21.py) and is
stored here as entry.png. This program only delivers that file: it
copies it into the output directory the grader sets, checks the copy
byte for byte with SHA-256, and exits 0. Standard library only, no
network access, no image libraries.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"


def sha256_of(path):
    """SHA-256 of a file, streamed in 1 MiB chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_dir():
    """Where the finished image goes: $MAKEFUN_OUTPUT_DIR, or this folder."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return Path(chosen)
    return Path(__file__).resolve().parent


def main():
    here = Path(__file__).resolve().parent
    source = here / IMAGE_NAME
    if not source.is_file():
        print(f"missing source image: {source}", file=sys.stderr)
        return 1

    dest = output_dir() / IMAGE_NAME
    # When the output directory IS this repo (no $MAKEFUN_OUTPUT_DIR set),
    # the destination is the source file itself: copying would be a no-op
    # and copyfile would raise SameFileError, so skip the copy instead.
    try:
        if dest.resolve() == source.resolve():
            print(f"already in place: {dest}")
            return 0
    except OSError:
        pass
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)

    if sha256_of(source) != sha256_of(dest):
        print("copy failed its hash check", file=sys.stderr)
        return 1
    print(f"wrote {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
