from libs.player import Player

class Player_matchmaking:

    def __init__(self, player, add_to_matchmaking, game_modes):
        self.player = player
        self.add_to_matchmaking = int(add_to_matchmaking)
        self.game_modes = game_modes

    def __eq__(self, other):
        return self.player == other.player