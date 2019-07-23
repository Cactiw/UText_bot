class Item:
    def __init__(self, type, id, name, rarity=None):
        self.type = type
        self.id = int(id)
        self.name = name
        self.rarity = rarity
