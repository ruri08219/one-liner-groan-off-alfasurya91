"""One-line dad joke entry for The One-Liner Groan-Off.

Writes a single original dad joke to /output/entry.txt.
Gate: UTF-8 text, 1-140 characters, not only whitespace, one line.
Standard library only.
"""

import os

ENTRY = "I told my vacuum it was doing a great job. It said, 'I suck at taking compliments.'"

MAX_CHARS = 140


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
    return text


def main():
    text = validate(ENTRY)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
