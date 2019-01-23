from bin.player_service import get_player, update_status, get_equipment
from bin.service_commands import show_general_buttons
from work_materials.globals import *


def merchant(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status('Merchant', player, user_data)
    user_data.update({'saved_merchant_status' : 'In Location'})
    show_general_buttons(bot, update, user_data)


def merchant_buy(bot, update, user_data):
    text = update.message.text
    player = get_player(update.message.from_user.id)
    if text == 'Голова':
        type = "eh"
    elif text == 'Тело':
        type = "eb"
    elif text == 'Перчатки':
        type = "es"
    elif text == 'Ноги':
        type = "ez"
    elif text == 'Средства передвижения':
        type = "em"
    elif text == 'Импланты':
        type = "ei"
    else:
        type = "e"
    location_id = player.location
    location_type = 0 if (location_id >= 14 and location_id <= 16) else 1
    request = "SELECT item_id, equipment_id, item_name, item_price FROM merchant_items WHERE location_type = '{0}' and item_type = '{1}'".format(location_type, type)
    cursor.execute(request)
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Пройдя в указанный продавцом угол, вы обнаружили"
                                                                   " лишь пыль на давно пустующих полках. Что же, может, в другой раз?")
        return
    response = "Список товаров:\n"
    while row:
        response += "\n<b>{0}</b>\n<b>💰{1}</b>\nПодробнее: /item_{2}\nКупить: /buy_{2}\n".format(row[2], row[3], row[0])
        row = cursor.fetchone()
    bot.send_message(chat_id = update.message.from_user.id, text = response, parse_mode="HTML")

def buy(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    request = "SELECT equipment_id, item_price FROM merchant_items WHERE item_id = '{0}'".format(update.message.text.partition('_')[2])
    cursor.execute(request)
    row = cursor.fetchone()
    equipment = get_equipment(row[0])
    gold = player.resources.get("gold")
    if row is None or equipment is None or gold < row[1]:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный предмет не найден")
        return
    player.resources.update({"gold": gold - row[1]})
    player.add_item(player.eq_backpack, equipment, 1)
    players_need_update.put(player)
    bot.send_message(chat_id=update.message.from_user.id, text="Вы наслаждаетесь видом новой шмотки")
