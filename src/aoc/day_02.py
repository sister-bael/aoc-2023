from dataclasses import asdict, dataclass



@dataclass
class ColorCounter:
    red: int = 0
    green: int = 0
    blue: int = 0

@dataclass
class Bag(ColorCounter):
    pass

@dataclass
class Round(ColorCounter):
    def is_possible(self, bag: Bag) -> bool:
        return all([asdict(bag)[color] >= count for color, count in asdict(self).items()])

    @classmethod
    def parse(cls, round_str) -> "Round":
        return cls(**dict((color, int(count)) for count, color in [p.strip().split() for p in round_str.split(',')]))



Game: list[Round]

def part_a(input_val: str):
    bag = Bag(12, 13, 14)
    score = 0
    game_i = 1
    for game in [line.strip() for line in input_val.splitlines() if line.strip()]:
        game_id, rounds = game.split(': ')
        rounds = [round.strip() for round in rounds.split(";") if round.strip()]
        g, game_id = game_id.split()
        assert g == "Game"
        assert int(game_id) == game_i

        if all(Round.parse(round).is_possible(bag) for round in rounds):
            score += game_i

        game_i += 1

    return score

def part_b(input_val: str):
    score = 0
    for game in [line.strip() for line in input_val.splitlines() if line.strip()]:
        _, rounds = game.split(": ")
        rounds = [Round.parse(round.strip()) for round in rounds.split(";") if round.strip()]

        maxes = ColorCounter(**dict((color, max([asdict(round)[color] for round in rounds])) for color in asdict(rounds[0])))

        score += maxes.red * maxes.blue * maxes.green

    return score