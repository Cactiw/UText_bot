from work_materials.globals import *


#TODO Разделить по id, чтобы текст был более похож на естественный
def show_capital_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в столице", reply_markup=capital_buttons)


def show_guildCastle_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в Замке Гильдии", reply_markup=guild_buttons)


def show_Tower_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в Башне", reply_markup=tower_buttons)


def show_farmLocation_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в локации для фарма, хорошо бы их как-нибудь назвать уже",
                     reply_markup=farmLocation_buttons)


def show_resourceLocation_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в лесу или шахте, знаю, потом разделю",
                     reply_markup=resource_buttons)


def show_resourceOffIsland_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в лесу или шахте, но не на острове",
                     reply_markup=resource_buttons_offIsland)


def show_castle_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы в замке, готовьтесь напасть на портал",
                     reply_markup=castle_buttons)


def show_portal_buttons(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Вы у портала, не лезь, она тебя сожрет",
                     reply_markup=portal_buttons)


def show_general_buttons(bot, update, user_data):
    status = user_data.get('status')
    if status != 'In Location':
        return
    loc_id = players.get(update.message.from_user.id).location
    if loc_id >= 14 and loc_id <= 16:
        show_capital_buttons(bot, update, user_data)
    elif loc_id >= 17 and loc_id <= 19:
        show_guildCastle_buttons(bot, update, user_data)
    elif loc_id >= 5 and loc_id <= 10:
        show_Tower_buttons(bot, update, user_data)
    elif loc_id >= 26 and loc_id <= 40:
        show_farmLocation_buttons(bot, update, user_data)
    elif loc_id >= 20 and loc_id <= 25:
        show_resourceLocation_buttons(bot, update, user_data)
    elif loc_id >= 11 and loc_id <= 13:
        show_resourceOffIsland_buttons(bot, update, user_data)
    elif loc_id >= 2 and loc_id <= 4:
        show_castle_buttons(bot, update, user_data)
    elif loc_id == 1:
        show_portal_buttons(bot, update, user_data)
    else:
        print("ERROR: WRONG STATUS in /bin/show_general_buttons.py")
        print(user_data)


