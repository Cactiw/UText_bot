from work_materials.globals import dispatcher
from bin.item_service import get_resource

import random


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


class CommonDropEncounter(DropEncounter):
    def __init__(self):
        items = []
        self.drop_limit = 2
        for i in range(self.drop_limit):
            # Генерация ресурсов
            a = random.randint(100)

        super(CommonDropEncounter, self).__init__(0, "Поздравляем, вы что-то нашли!", )
