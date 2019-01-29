from bin.player_service import get_player

class BattleGroup:

    def __init__(self, creator):
        self.creator = creator
        self.players = [creator]
        self.invitations = []

    def avg_lvl(self):
        lvl_sum = 0
        total_players = 0
        for curr in self.players:
            player = get_player(curr)
            lvl_sum += player.lvl
            total_players += 1
        return lvl_sum / total_players

    def num_players(self):
        return len(self.players)
