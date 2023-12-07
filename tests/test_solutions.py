import datetime
import importlib
from importlib.resources import files as resource_files
import pathlib
from sys import stderr
import types
import typing
import unittest

import yaml

A = "a"
B = "b"

def _collect() -> typing.Iterator[tuple[int, str, typing.Any, types.ModuleType]]:

    for day in range(1, datetime.datetime.now().day + 1):
        try:
            module = importlib.import_module(f"aoc.day_{day:02}")
        except ModuleNotFoundError:
            print(f"No solution found for day {day:02}")
            continue
        examples = yaml.safe_load(resource_files('tests.examples').joinpath(f"{day:02}.yml").read_text())
        data_text = resource_files("aoc.inputs").joinpath(f"{day:02}.txt").read_text()
        yield day, data_text, examples, module

class TestExamples(unittest.TestCase):
    def test_examples(self):
        for day, input_data, examples, module in _collect():
            example_input = None
            for example in examples[A]:
                with self.subTest(part=A, example=example):
                    this_example_input = example_input if example["input"] is None else example["input"]
                    if example_input is None:
                        example_input = this_example_input
                    self.assertEqual(module.part_a(this_example_input), example["expected"])
                    print(f"day {day} part a res: {module.part_a(input_data)}")
            for example in examples[B]:
                with self.subTest(part=B, example=example):
                    this_example_input = example_input if example["input"] is None else example["input"]
                    self.assertEqual(module.part_b(this_example_input), example["expected"])
                    print(f"day {day} part b res: {module.part_b(input_data)}")