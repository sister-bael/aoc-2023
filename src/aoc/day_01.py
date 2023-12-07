import re
from typing import Iterator

WORDS_TO_DIGITS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

MATCHY = "|".join([r"\d"] + list(WORDS_TO_DIGITS))

def _get_lines(input_val: str) -> Iterator[str]:
    for line in [ln.strip() for ln in input_val.splitlines() if ln.strip()]:
        yield line

def part_a(input_val: str) -> int:

    total = 0

    for line in _get_lines(input_val):
        a = re.match(r"^[^\d]*?(\d)", line).groups()[0]
        b = re.match(r".*(\d)[^\d]*?$", line).groups()[0]
        total += int(f"{a}{b}")
    return total

def part_b(input_val: str) -> int:

    total = 0
    for line in _get_lines(input_val):
        a = re.match(r"^.*?(" + MATCHY + r").*", line).groups()[0]
        b = re.match(r".*(" + MATCHY + r").*?$", line).groups()[0]
        a = int(a) if a.isdigit() else WORDS_TO_DIGITS[a]
        b = int(b) if b.isdigit() else WORDS_TO_DIGITS[b]
        total += int(f"{a}{b}")

    return total


        