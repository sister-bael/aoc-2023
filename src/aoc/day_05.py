"""
640121624 is too high
"""

import copy
from dataclasses import dataclass
import re
from sys import stderr
import typing

FACTOR_LIST = ["soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
MAPRE = re.compile(r"([a-z]+)-to-([a-z]+) map:")
SEEDSRE = re.compile(r"^seeds:((?:\s+\d+)+)$")



@dataclass
class Range:
    dest: int
    source: int
    length: int

    def resolve(self, source_val: int) -> int | None:
        if self.source <= source_val <= self.source + (self.length -1):
            result = self.dest + (source_val - self.source)
            # print(f"DEBUG: {self} resolved `{source_val}` to `{result}`")
            return result
        # print(f"DEBUG: range {self} did not resolve {source_val}")
        return None

    def debug(self):
        print(self)
        source, dest = self.source, self.dest
        print(f"{source - 1:03d}: {source -1:03d} ({self.resolve(source - 1 )})")
        for i in range(self.length):
            print(f"{source + i:03d}: {dest +i:03d} ({self.resolve(source + i)})")

class FactorMap:
    def __init__(self, map_repr: str):
        repr_lines = [ln.strip() for ln in map_repr.strip().splitlines() if ln.strip()]
        heading, body = repr_lines[0], repr_lines[1:]
        heading_match = MAPRE.match(heading)
        assert heading_match is not None
        assert not any(MAPRE.match(body_ln) is not None for body_ln in body)
        self.source, self.dest = heading_match.groups()
        self.ranges = [Range(*[int(num.strip()) for num in body_ln.split()]) for body_ln in body]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.source}:{self.dest}[{', '.join(str(range) for range in self.ranges)}]"

    def resolve(self, source_val: int) -> int:
        for range in self.ranges:
            # print(f"DEBUG: {self.source}:{self.dest} trying {range} for {source_val}")
            resolved = range.resolve(source_val)
            # print(f"DEBUG: resolve resulted in {resolved}")
            if resolved is not None:
                result = resolved
                break
        else:
            result = source_val
        # print(f"DEBUG: {self.source}:{self.dest} resolved `{source_val}` to `{result}`")
        return result

def _get_val_for_factor(seed: int, factor: str, mappings: dict[str: FactorMap]) -> int:
    this_key = seed
    # create a new dict so that changes aren't side effects
    mappings = copy.copy(mappings)
    this_map = mappings.pop("seed")
    while mappings:

        this_key = this_map.resolve(this_key)
        if this_map.source == factor:
            break
        this_map = mappings.pop(this_map.dest)
    else:
        # ran out of mappings gotta finish out
        this_key = this_map.resolve(this_key)

    return this_key


def part_a(input_val: str) -> typing.Any:
    seeds_line, maps_lines = input_val.split("\n", 1)
    seeds = [int(seed) for seed in SEEDSRE.match(seeds_line).groups()[0].strip().split()]
    mappings: dict[str, FactorMap] = {}
    for factor_mapping in maps_lines.split("\n\n"):
        mapping = FactorMap(factor_mapping)
        assert mapping.source not in mappings
        mappings[mapping.source] = mapping

    def get_location(seed: int) -> int:
        return _get_val_for_factor(seed, "location", mappings)
    scores = {}
    for seed in seeds:
        scores[seed] = get_location(seed)
    #scores = dict((seed, (get_location(seed), [(factor, _get_val_for_factor(seed, factor, mappings)) for factor in FACTOR_LIST])) for seed in seeds)
    # print(f"DEBUG: scores: {scores}", file=stderr)

    return min(score for score in scores.values())

def part_b(input_val: str) -> typing.Any:
    raise NotImplementedError()
