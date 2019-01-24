

class BattleGroup:

    def __init__(self, creator):
        self.creator = creator
        self.players = [creator]
        self.invitations = []
