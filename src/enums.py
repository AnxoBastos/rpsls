from enum import IntEnum

class GameAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2    