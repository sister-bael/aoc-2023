import dataclasses
from functools import reduce
from typing import Iterator

@dataclasses.dataclass
class Point:
    x: int
    y: int
    value: str

    def is_symbol(self) -> bool:
        return self.value != "." and not self.value.isdigit()

    def is_gear(self) -> bool:
        return self.value == "*"

    def is_blank(self) -> bool:
        return self.value == "."
    
    def is_digit(self) -> bool:
        return self.value.isdigit()

    def gear_ratio(self) -> int | None:
        if not self.is_gear():
            return None
        


    def is_adjacent(self, *points):
        """
        Returns True if this point is adjacent to any in a collection of points
        """

        for point in points:
            min_x, max_x = sorted([self.x, point.x])
            min_y, max_y = sorted([self.y, point.y])
            if max_x - min_x <=1 and max_y - min_y <= 1:
                return True
        return False

@dataclasses.dataclass
class Number:
    points: list[Point]

    def is_adjacent(self, point: Point):
        return point.is_adjacent(*self.points)

    @property
    def val(self) -> int:
        return int(''.join(point.value for point in self.points))

    def __repr__(self):
        return f"<Number `{self.val()}` ({self.points[0].x}-{self.points[-1].x}, {self.points[0].y})"

def _get_grid(input_val: str):
    rows = []
    for row_i, line in enumerate([ln for ln in input_val.splitlines() if ln.strip()]):
        rows.append([Point(x=col_i, y=row_i, value=char_val) for col_i, char_val in enumerate(line)])
    return rows

def get_numbers_and_symbols(grid = list[list[Point]]) -> tuple[list[Number], dict[str, Point]]:
    numbers = []
    symbols = {}
    for row in grid:
        number = None
        
        for point in row:
            if point.is_digit():
                if number is None:
                    number = Number([point])
                else:
                    number.points.append(point)
            else:
                if number is not None:
                    numbers.append(number)
                number = None
                if point.is_symbol():
                    symbols.setdefault(point.value, []).append(point)
        if number is not None:
            numbers.append(number)

    return (numbers, symbols)

def part_a(input_val: str) -> int:

    score = 0
    grid = _get_grid(input_val)
    numbers, symbols = get_numbers_and_symbols(grid)
    all_symbols = sum(list(symbols.values()), [])
    return sum([number.val for number in numbers if any([number.is_adjacent(symbol) for symbol in all_symbols])])

def part_b(input_val: str) -> int:
    grid = _get_grid(input_val)
    numbers, symbols = get_numbers_and_symbols(grid)
    total = 0
    for symbol in symbols.get('*', []):
        adjacent = [number for number in numbers if number.is_adjacent(symbol)]
        if len(adjacent) < 2:
            continue
        total += reduce(lambda x, y: x*y, [number.val for number in adjacent])
    return total
    
    

# testing

p1 = Point(1, 1, "+")
p2 = Point(2, 2, "1")
p3 = Point(3, 3, ".")
p4 = Point(1,2, "3")

assert(p1.is_adjacent(p2))
assert(p1.is_adjacent(p4))
assert(not p1.is_adjacent(p3))