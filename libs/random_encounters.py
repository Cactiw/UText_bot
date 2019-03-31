from work_materials.globals import dispatcher


class DropEncounter:

    def __init__(self, rarity, message, items, drop_limit):
        self.rarity = rarity
        self.message = message  # Текст, который выведется в сообщении
        self.items = items  # Возможные айтемы для дропа
        self.drop_limit = drop_limit  # Ограничения на дроп, хз в каком виде вообще

    def run(self, player):
        dispatcher.bot.send_message(chat_id=player.id, text=self.message, parse_mode='HTML')
        for item in self.items:
            player.add_item(item, 1)
