"""One-line dad joke entry for The One-Liner Groan-Off.

Writes a single original dad joke to /output/entry.txt.
Gate: UTF-8 text, 1-140 characters, not only whitespace, one line.
After writing, the file is read back and verified byte-identical to the
entry, with no trailing newline, so a partial or mangled write fails loudly.
Standard library only.
"""

import os

ENTRY = "I told my vacuum it was doing a great job. It said, 'I suck at taking compliments.'"

MAX_CHARS = 140
# A 140-char UTF-8 string is at most 4 bytes per char.
MAX_BYTES = 4 * MAX_CHARS


def validate(text):
    """Check the entry against the competition gate. Raises ValueError."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-140 characters, got %d" % len(text))
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("entry contains a control character U+%04X" % ord(ch))
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise ValueError("entry exceeds %d UTF-8 bytes" % MAX_BYTES)
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip check: the file must be byte-identical to the entry,
    # with no trailing newline added by the write.
    with open(path, "rb") as f:
        written = f.read()
    expected = text.encode("utf-8")
    if written != expected:
        raise ValueError("entry.txt round-trip mismatch: wrote %d bytes, expected %d" % (len(written), len(expected)))
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
