#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Copies the pre-rendered meme (entry.png, sitting next to this script) to
/output/entry.png. Standard library only: no image libraries, no fonts,
no drawing, no network. The image was rendered at build time and is shipped
as-is, so the graded run is a plain file copy and works in a bare
python:3.13 image. Deterministic: the output is byte-identical to entry.png
on every run.
"""

import os
import shutil

OUTPUT_DIR = "/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.png")


SOURCE_NAME = "entry.png"


def copy_entry():
    """Copy the pre-rendered meme next to this script to /output."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(source, OUTPUT_FILE)


def main():
    copy_entry()


if __name__ == "__main__":
    main()
