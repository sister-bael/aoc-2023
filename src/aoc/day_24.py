from dataclasses import dataclass
from math import atan2
import typing

"""
I've modified the input and example values to start with the window range"""

Numeric = int | float

@dataclass
class SpatialAtomic:
    x: Numeric
    y: Numeric
    z: Numeric

    @classmethod
    def from_input(cls, input_str: str) -> "SpatialAtomic":
        return cls(*input_str.strip().split(", "))

@dataclass
class Vector(SpatialAtomic):
    pass

@dataclass
class Point(SpatialAtomic):
    pass

@dataclass
class Segment:
    a: Point
    b: Point

@dataclass
class Stone:
    origin: Point
    vector: Vector


    @classmethod
    def from_input(cls, input_line: str) -> "Stone":
        position, velocity = input_line.split("@")
        position, velocity = Point.from_input(position), Vector.from_input(velocity)
        return cls(position, velocity)

    def box_intersection2(x: Numeric, y: Numeric, x_max: typing.Optional[Numeric] = None, y_max: typing.Optional[Numeric] = None):
        if x_max is None:
            x_max = x
        if y_max is None:
            y_max = y




def part_a(input_val: str) -> typing.Any:
    input_lines = input_val.strip().splitlines()
    window_line, input_lines = input_lines[0], input_lines[1:]
    window_min, window_max = (int(val.strip()) for val in window_line.split(", "))
    # Could make something more sophisticated but this is by my guess computationally quicker. could check but haven't yet
    for stone in [Stone(in_line) for in_line in input_lines]:




def part_b(input_val: str) -> typing.Any:
    raise NotImplementedError()
