"""Roast Your Fridge: write the one-line entry to entry.txt.

Deterministic, no network, no randomness, no clock.
Reads MAKEFUN_OUTPUT_DIR (default: output) and writes the exact entry.
"""

import os
import sys

ENTRY = "My fridge has one dial, unlabelled, and every setting is either 'salad iceberg' or 'milk sauna'."


class BlankError(ValueError):
    """Entry is empty or whitespace-only."""


class MultiLineError(ValueError):
    """Entry contains a newline or carriage return."""


class LengthError(ValueError):
    """Entry is outside the 1-200 character range."""


class ReadBackError(ValueError):
    """Bytes read back differ from bytes written."""


def validate_entry(text):
    if not text or not text.strip():
        raise BlankError("entry is empty or blank-only")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise LengthError("entry must be 1-200 characters")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    validate_entry(ENTRY)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        read_back = f.read()
    if read_back != data:
        raise ReadBackError("read-back bytes differ from written entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
