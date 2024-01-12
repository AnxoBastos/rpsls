import random
from enums import GameAction
from abc import ABCMeta, abstractmethod

Victories = {
    GameAction.Scissors: [GameAction.Lizard, GameAction.Paper],
    GameAction.Paper: [GameAction.Spock, GameAction.Rock],
    GameAction.Rock: [GameAction.Lizard, GameAction.Scissors],
    GameAction.Lizard: [GameAction.Spock, GameAction.Paper],
    GameAction.Spock: [GameAction.Scissors, GameAction.Rock]
}

class ActionEngine(metaclass=ABCMeta):

    def __init__(self):
        self._opponent_history = []

    @abstractmethod
    def generate_action(self):
        pass

    def action_message(self, action):
        print(f"Computer picked {action.name}.")

    def add_opponent_action(self, action):
        self._opponent_history.append(action)

class RandomEngine(ActionEngine):
    
    def __init__(self):
        super().__init__()

    def generate_action(self):
            computer_selection = random.randint(0, len(GameAction) - 1)
            computer_action = GameAction(computer_selection)
            return computer_action

class TenMovesEngine(ActionEngine):
    
    def __init__(self):
        super().__init__()

    def generate_action(self):
        last_ten = self._opponent_history[-10:]
        most_frequent = max(set(last_ten), default=None, key=last_ten.count)

        if most_frequent == None:
            most_frequent = GameAction.Rock

        return Victories[most_frequent]
    
class PreviousMoveEngine(ActionEngine):

    def __init__(self):
        super().__init__()

    def generate_action(self):
        if not self._opponent_history:
            self._opponent_history.append(GameAction.Rock)

        return Victories[self._opponent_history[-1]]

class PredictiveEngine(ActionEngine):
    
    def __init__(self):
        self._play_order = {
                (GameAction.Rock, GameAction.Rock) : 0, 
                (GameAction.Rock, GameAction.Paper) : 0, 
                (GameAction.Rock, GameAction.Scissors) : 0, 
                (GameAction.Paper, GameAction.Rock) : 0, 
                (GameAction.Paper, GameAction.Paper) : 0, 
                (GameAction.Paper, GameAction.Scissors) : 0,
                (GameAction.Scissors, GameAction.Rock) : 0, 
                (GameAction.Scissors, GameAction.Paper) : 0, 
                (GameAction.Scissors, GameAction.Scissors) : 0
            }
        super().__init__()

    def generate_action(self):
        if not self._opponent_history:
            self._opponent_history.append(GameAction.Rock)

        last_two = tuple(self._opponent_history[-2:])
        if len(last_two) == 2:
            self._play_order[last_two] += 1

        potential_plays = [
            (self._opponent_history[-1], GameAction.Rock),
            (self._opponent_history[-1], GameAction.Paper),
            (self._opponent_history[-1], GameAction.Scissors)
        ]

        sub_order = {
            play: self._play_order[play]
            for play in potential_plays
        }

        prediction = max(sub_order, key=sub_order.get)[-1]

        return Victories[prediction]