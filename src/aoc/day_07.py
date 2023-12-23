import enum
import typing

CARD_RANKS = dict((card, score) for score, card in enumerate(reversed("AKQJT98765432")))

class HandType(enum.IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def _get_pairs(self, hand: str) -> set[str]:
        return set([chr for chr in set(hand) if hand.count(chr) == 2])

    @classmethod
    def get_type(cls, hand: str, debugging=False) -> "HandType":
        the_type = None
        for hand_type in cls:
            if hand_type.matches(hand):
                if not debugging:
                    return hand_type
                # implicit is debugging
                assert the_type is None, "a hand should not be able to match more than one type"
                the_type = hand_type
        return the_type



    def matches(self, hand: str) -> bool:
        cls = self.__class__
        if self is cls.ONE_PAIR:
            return (len(self._get_pairs(hand)) == 1) and len(set(hand)) > 2
        elif self is cls.TWO_PAIR:
            return len(self._get_pairs(hand)) == 2
        elif self is cls.THREE_OF_A_KIND:
            return max([hand.count(chr) for chr in set(hand)]) == 3 and len(set(hand)) > 2
        elif self is cls.FULL_HOUSE:
            return (len(self._get_pairs(hand)) == 1) and len(set(hand)) == 2
        elif self is cls.FOUR_OF_A_KIND:
            return max([hand.count(chr) for chr in set(hand)]) == 4
        elif self is cls.FIVE_OF_A_KIND:
            return max([hand.count(chr) for chr in set(hand)]) == 5
        elif self is cls.HIGH_CARD:
            return len(hand) == len(set(hand))
        assert False, "all hand types must have a matching pattern"


class Hand(str):
    @property
    def type(self) -> HandType:
        return HandType.get_type(self)
    def __gt__(self, other: "Hand") -> bool:
        if other is None:
            return True
        if self.type == other.type:
            for this_char, other_char in zip(self, other):
                if this_char == other_char:
                    continue
                this_rank, other_rank = CARD_RANKS[this_char], CARD_RANKS[other_char]
                return this_rank > other_rank
            return True
        return self.type > other.type

    def __repr__(self) -> str:
        return f"<Hand {self.type.name}: `{super().__str__()}`>"

    def __lt__(self, other: "Hand") -> bool:
        """
        probably a good quick way to dedupe this with gt but I'm lazy
        """
        if other is None:
            return False
        if self.type == other.type:
            for this_char, other_char in zip(self, other):
                if this_char == other_char:
                    continue
                this_rank, other_rank = CARD_RANKS[this_char], CARD_RANKS[other_char]
                return this_rank < other_rank
            return True

        return self.type < other.type

    def maximize_jokers(self) -> "Hand":
        if "J" not in self.upper():
            return self
        other_cards = list(sorted([card for card in self.upper() if card != "J"], key=lambda x: CARD_RANKS[x]))
        if other_cards:
            top_card = other_cards[-1]
            most_common = max(other_cards, key=self.count)
        else:
            top_card = "A"
            most_common = "A"
        match len(set(other_cards)):
            case 0:
                new_card = "A"
            case 1:
                new_card = top_card
            case 2:
                if min(self.count(char) for char in set(other_cards)) == 1:
                    # at least one is single length, can get 4 of a kind
                    if len(other_cards) == 2:
                        new_card = top_card
                    else:
                        new_card = most_common
                else:
                    # two pairs, get the higher for a full house
                    new_card = top_card
            case 3:
                if len(other_cards) == 3:
                    # 3 unique cards, two jokers, match jokers to the highest of the unique cards
                    new_card = top_card
                else:
                    # one card is duplicated, match the jokers to that to make three of a kind
                    new_card = most_common
            case 4:
                # Currently 5 different cards, best we can do is duplicate the highest card
                new_card = top_card
        return self.__class__(self.upper().replace("J", new_card.upper()))

def _rank_hands(hands):
    return list(sorted(hands))

def part_a(input_val: str) -> typing.Any:
    hands = [line.strip().split() for line in input_val.splitlines() if line.strip()]
    hands = [(Hand(hand), int(bid)) for hand, bid in hands]
    return sum((rank + 1) * hand_info[1] for rank, hand_info in enumerate(_rank_hands(hands)))

def part_b(input_val: str) -> typing.Any:
    hands = [line.strip().split() for line in input_val.splitlines() if line.strip()]
    print(hands)
    maxed_hands = [(Hand(hand).maximize_jokers(), int(bid)) for hand, bid in hands]
    print(_rank_hands(maxed_hands))
    import pdb
    pdb.set_trace()
    return sum((rank + 1) * hand_info[1] for rank, hand_info in enumerate(_rank_hands(maxed_hands)))