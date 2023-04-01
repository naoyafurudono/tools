import datetime
import random
import time
from typing import Tuple


class InvalidArgument(Exception):
    pass


class Game:
    answer: list[int]
    inputs: list[list[int]]
    size: int

    def __init__(self, size: int) -> None:
        if not 0 < size <= 10:
            raise InvalidArgument()
        self.size = size
        self.inputs = []

        bag = list(range(10))
        ans: list[int] = []
        for _i in range(size):
            chosen: int = random.choice(bag)
            bag.remove(chosen)
            ans.append(chosen)
        self.answer = ans

    def check(self, candidate: list[int]) -> Tuple[int, int]:
        if len(candidate) != self.size:
            raise InvalidArgument(
                f"length must be {self.size} but the candidate has {len(candidate)}"
            )
        if not is_unique(candidate):
            raise InvalidArgument()

        hits = len(set(self.answer).intersection(candidate))
        eats = 0
        for i in range(self.size):
            if self.answer[i] == candidate[i]:
                eats += 1
        bites = hits - eats
        return (bites, eats)

    def challenge(self, candidate: list[int]) -> Tuple[str, bool]:
        if not len(candidate) == self.size:
            return "too long", False
        self.inputs.append(candidate)
        (bites, eats) = self.check(candidate)
        match (bites, eats):
            case (0, self.size):
                return (
                    f"congrat! the answer is {candidate}\nscore: {len(self.inputs)}",
                    True,
                )
            case _:
                return (f"bites: {bites}, eats: {eats}", False)

    def quit(self) -> Tuple[str, bool]:
        return f"ans: {self.answer}", True

    def dispatch(self, cmd: str) -> Tuple[str, bool]:
        if cmd in ["q", "quit"]:
            return self.quit()
        try:
            candidate = str_to_candidate(cmd)
        except Exception as _e:
            return "bad input", False
        return self.challenge(candidate)


def is_unique(l: list[int]) -> bool:
    return len(set(l)) == len(l)


def str_to_candidate(s: str) -> list[int]:
    return [int(c) for c in s]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="numeron",
    )
    parser.add_argument("ans_size", type=int)

    args = parser.parse_args()
    game = Game(args.ans_size)
    done = False
    start = time.time()
    while not done:
        cmd = input("> ")
        (msg, done) = game.dispatch(cmd)
        print(msg, end="\n\n")
    duration = time.time() - start
    print(f"time: {datetime.timedelta(seconds=duration)}")
