from work_materials.globals import *


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
    if status == "In Capital":
        show_capital_buttons(bot, update, user_data)
    elif status == "In Guild Castle":
        show_guildCastle_buttons(bot, update, user_data)
    elif status == "In Tower":
        show_Tower_buttons(bot, update, user_data)
    elif status == "In Farm Location":
        show_farmLocation_buttons(bot, update, user_data)
    elif status == "In Resource Location":
        show_resourceLocation_buttons(bot, update, user_data)
    elif status == "In Resource Off Island Location":
        show_resourceOffIsland_buttons(bot, update, user_data)
    elif status == "In Castle":
        show_castle_buttons(bot, update, user_data)
    elif status == "In Portal Location":
        show_portal_buttons(bot, update, user_data)
    else:
        print("ERROR: WRONG STATUS in /bin/show_general_buttons.py")
        print(user_data)


