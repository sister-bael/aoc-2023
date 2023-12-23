import functools
import operator
from statistics import mean
import typing

@functools.cache
def _get_distance(hold_time: int, race_time: int) -> int:
    """
    mm per sec is effectively hold time, no need to make a new var just to rename it
    """
    return hold_time * (race_time - hold_time)

@functools.cache
def _intmean(a: int, b: int) -> int:
    return int(mean([a, b]))

def part_a(input_val: str) -> typing.Any:
    times, distances = [line.strip().split() for line in input_val.strip().splitlines()]
    assert times[0] == "Time:" and distances[0] == "Distance:"

    times, records = [[int(num) for num in row] for row in [times[1:], distances[1:]]]
    distances = [[hold_time for hold_time in range(race_time + 1) if _get_distance(hold_time, race_time) > record] for race_time, record in zip(times, records)]

    return functools.reduce(operator.mul, [len(res) for res in distances], 1)

    return times, distances

def part_b(input_val: str) -> typing.Any:
    race_time, record = [int(''.join(line.strip().split()[1:])) for line in input_val.strip().splitlines()]
    half_race = int(race_time / 2)
    min_check, max_check = 1, half_race

    while min_check < max_check -1:
        last_min, last_max = min_check, max_check
        while _get_distance(_intmean(min_check, max_check), race_time) <= record  and max_check - min_check > 1:

            print(f"checking to round {min_check} up to {max_check}")
            min_check = _intmean(min_check, max_check)
        while _get_distance(_intmean(min_check, max_check), race_time) > record and max_check - min_check > 1:
            max_check = _intmean(min_check, max_check)
        assert not (min_check == last_min  and max_check == last_max)
        print(f'restarting {min_check} {max_check}')
    assert all([_get_distance(i, race_time) > record for i in range(min_check, race_time - min_check)])
