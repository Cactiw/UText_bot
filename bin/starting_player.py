from work_materials.globals import *
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from libs.player import *
from bin.show_general_buttons import show_general_buttons


def start(bot, update, user_data):
    user_data.update(type = 1)
    request = "SELECT * FROM PLAYERS WHERE id = '{0}'".format(update.message.from_user.id)
    cursor.execute(request)
    row = cursor.fetchone()
    if row is not None:
        bot.send_message(chat_id=update.message.chat_id, text='Вы уже в игре!')
        return
    user_data.clear()
    user_data.update(type = 1)
    button_list = [
        KeyboardButton('Люди'),
        KeyboardButton('Орки'),
        KeyboardButton('Эльфы')
    ]
    #print(user_data)
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3), resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text='Выберите фракцию, за которую вы будете сражаться!', reply_markup = reply_markup)
    return


def fraction_select(bot, update, user_data):
    type = user_data.get('type')
    if type is 1:   # Выбор фракции
        user_data.update({'fraction': update.message.text, 'type': 2})

        button_list = [
            KeyboardButton('Люди'),
            KeyboardButton('Орки'),
            KeyboardButton('Эльфы')
        ]
        reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3), resize_keyboard=True)

        bot.send_message(chat_id=update.message.chat_id, text='Вы выбрали фракцию <b>{0}</b>\n'
                                                              'Теперь необходимо выбрать расу!'.format(
            user_data.get('fraction')), parse_mode='HTML', reply_markup=reply_markup)
        #print(user_data)
        return
    elif type is 2:    # Выбор расы
        #print(user_data)
        race_select(bot, update, user_data)


def race_select(bot, update, user_data):
    user_data.update({'race': update.message.text, 'type': 3})

    button_list = [
        KeyboardButton('Воин'),
        KeyboardButton('Маг'),
        KeyboardButton('Лучник'),
        KeyboardButton('Клирик'),
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True)

    bot.send_message(chat_id=update.message.chat_id, text='Вы выбрали расу <b>{0}</b>\n'
                                                          'Теперь необходимо выбрать класс!'.format(
        user_data.get('race')), parse_mode='HTML', reply_markup=reply_markup)
    #print(user_data)
    return


def class_select(bot, update, user_data):
    user_data.update({'class' : update.message.text, 'type' : 4})
    button_list = [
        KeyboardButton('Мужской'),
        KeyboardButton('Женский'),
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1), resize_keyboard=True)
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Отлично, вы выбрали класс <b>{0}</b>\n'
             'Выберите пол:'.format(user_data.get('class')),
        parse_mode = 'HTML', reply_markup = reply_markup)
    #print(user_data)
    return


def sex_select(bot, update, user_data):
    user_data.update(sex=update.message.text, type=5)
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Отлично, осталось всего лишь выбрать имя, '
             'под которым вас будут знать другие игроки!'.format(user_data.get('class')),
        parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    #print(user_data)
    return


def nickname_select(bot, update, user_data):
    user_data.update(username=update.message.text, type=6)
    player = Player(update.message.from_user.id, update.message.from_user.username, user_data.get('username'),
                    user_data.get('sex'), user_data.get('race'), user_data.get('fraction'), user_data.get('class'))
    player.status = 'In capital'  #TODO сделать статус 'starting' и сделать начальный квест
    print(player.race)
    if player.race == 'Люди':
        player.location = 14
        user_data.update({'location_name': locations.get(14).name})
        user_data.update({'location': 14})
    elif player.race == 'Эльфы':
        player.location = 15
        user_data.update({'location_name': locations.get(15).name})
        user_data.update({'location': 15})
    elif player.race == 'Орки':
        player.location = 16
        user_data.update({'location_name': locations.get(16).name})
        user_data.update({'location': 16})
    user_data.update({'status': 'In Location'})
    player.status = 'In Location'
    players.update({player.id: player})
    show_general_buttons(bot, update, user_data)  #Проверить, что работает
    player.add_to_database(conn, cursor)
    bot.send_message(chat_id=update.message.chat_id,
                     text='Вы выбрали имя <b>{0}</b>\n'
                          'И можете приступить к игре!'.format(user_data.get('username')),
                     parse_mode='HTML')
    user_data.pop('type')
    print(user_data)
    return