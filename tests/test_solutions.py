import datetime
import importlib
from importlib.resources import files as resource_files
import os
from sys import stderr
import types
import typing
import unittest

import yaml

A = "a"
B = "b"

EXAMPLES_ONLY = os.getenv("EXAMPLES_ONLY", "False").lower() in ["t", "true", "yes", "y", "hyuyup", "most assuredly", "1"]
NO_EXAMPLES = os.getenv("NO_EXAMPLES", "False").lower() in ["t", "true", "yes", "y", "hyuyup", "most assuredly", "1"]
MAX_DAY = int(os.getenv("MAX_DAY", "31"))
ONLY_DAY = int(os.getenv("TEST_DAY", "0")) or None

assert not (EXAMPLES_ONLY and NO_EXAMPLES), "It is not valid to have both EXAMPLES_ONLY and NO_EXAMPLES on the env"


class MissingStuff(FileNotFoundError):
    pass

class MissingSolution(MissingStuff):
    pass

class MissingInput(MissingStuff):
    pass

class MissingExamples(MissingStuff):
    pass

def _collect_day(day: int) -> tuple[int, str, typing.Any, types.ModuleType]:
    try:
        module = importlib.import_module(f"aoc.day_{day:02}")
    except ModuleNotFoundError as exc:
        raise MissingSolution(f"no solution for {day}") from exc
    try:
        examples = yaml.safe_load(resource_files('tests.examples').joinpath(f"{day:02}.yml").read_text())
    except FileNotFoundError as exc:
        raise MissingExamples(f"no examples for {day}") from exc
    try:
        data_text = resource_files("aoc.inputs").joinpath(f"{day:02}.txt").read_text()
    except FileNotFoundError as exc:
        raise MissingInput(f"no input for {day}") from exc
    return (day, data_text, examples, module)

def _collect() -> typing.Iterator[tuple[int, str, typing.Any, types.ModuleType]]:

    if ONLY_DAY is not None:
        yield _collect_day(ONLY_DAY)
        return
    for day in range(1, datetime.datetime.now().day + 1):
        if day > MAX_DAY:
            break
        try:
            yield _collect_day(day)
        except MissingStuff as exc:
            print(f"missing stuff: {exc}")
        continue

        yield day, data_text, examples, module

class TestExamples(unittest.TestCase):
    def test_examples(self):
        for day, input_data, examples, module in _collect():
            example_input = None
            if not NO_EXAMPLES:
                for example in examples[A]:
                    with self.subTest(part=A, example=example):
                        this_example_input = example_input if example["input"] is None else example["input"]
                        if example_input is None:
                            example_input = this_example_input
                        self.assertEqual(module.part_a(this_example_input), example["expected"])
            if not EXAMPLES_ONLY:
                with self.subTest(part=A, main=True):
                    print(f"day {day} part a res: {module.part_a(input_data)}")
            if not NO_EXAMPLES:
                for example in examples[B]:
                    with self.subTest(part=B, example=example):
                        this_example_input = example_input if example["input"] is None else example["input"]
                        try:
                            self.assertEqual(module.part_b(this_example_input), example["expected"])
                        except NotImplementedError:
                            print(f"Day {day} part B not implemented", file=stderr)
            if not EXAMPLES_ONLY:
                with self.subTest(part=B, main=True):
                    try:
                        print(f"day {day} part b res: {module.part_b(input_data)}")
                    except NotImplementedError:
                        print(f"day {day} part B not implemented", file=stderr)