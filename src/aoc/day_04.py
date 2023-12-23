from functools import reduce
import re
import typing

CARD_RE = re.compile(r"Card\s+(\d+):\s+((?:\d+\s+)+)\|((?:\s+\d+)+)")

def _parse_card(card_repr: str) -> tuple[list[int], list[int]]:
    match = CARD_RE.match(card_repr)
    my_numbers, winning_numbers = [[int(num) for num in section.split()] for section in match.groups()[1:]]

    return my_numbers, winning_numbers

def score_card(card_repr: str) -> int:
    my_numbers, winning_numbers = _parse_card(card_repr)

    matching = set(my_numbers).intersection(winning_numbers)
    if not matching:
        return 0
    score = 1
    for _ in range(len(matching) - 1):
        score *=2

    return score

def part_a(input_val: str) -> typing.Any:
    return sum([score_card(line.strip()) for line in input_val.splitlines() if line.strip()])


def part_b(input_val: str) -> typing.Any:
    raise NotImplementedError()
