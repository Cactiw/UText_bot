from libs.player import *
from work_materials.globals import *
from work_materials.lines.location_lines import *
from work_materials.buttons.location_buttons import *
from work_materials.buttons.merchant_buttons import *
from work_materials.buttons.battle_buttons import get_general_battle_buttons
from bin.player_service import print_player

def update_location(location, player, user_data):
    player.location = location
    players.update({player.id: player})
    players_need_update.put(player)
    user_data.update({'location': location})
    user_data.update({'location_name': locations.get(location).name})

def get_player(id):
    player = players.get(id)
    if player is not None:
        update_location(player.location, player, dispatcher.user_data[id])
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database() is None:
        return None
    update_location(player.location, player, dispatcher.user_data[id])
    players.update({player.id: player})
    return player


def get_location_buttons(id):
    if id == 1:
        return portal_buttons
    if id in [2, 3, 4]:
        return castle_buttons
    if id in [5, 6, 7, 8, 9, 10]:
        return tower_buttons
    if id in [11, 12, 13]:
        return resource_buttons_offIsland
    if id in [14, 15, 16]:
        return capital_buttons
    if id in [17, 18, 19]:
        return guild_buttons
    if id in range(20, 41):
        return resource_buttons


def show_general_buttons(bot, update, user_data):
    status = user_data.get('status')
    try:
        chat_id = update.message.chat_id
    except AttributeError:
        try:
            chat_id = int(update)
        except TypeError:
            return
    player = get_player(chat_id)
    if status == 'In Location':
        location = user_data.get('location')
        bot.send_message(chat_id=chat_id, text=location_lines[player.location],reply_markup=get_location_buttons(location))
        #show_table (Доска объявлений, если нужно)
    elif status == 'Traveling':
        bot.send_message(chat_id=chat_id, text="Вы все еще идете до локации: {0}".format(locations.get(user_data.get('new_location')).name), reply_markup=traveling_buttons)
    elif status == 'Merchant':
        bot.send_message(chat_id=chat_id, text="Выберите категорию товара:", reply_markup=merchant_buttons)
    elif status == 'Merchant_buy':
        bot.send_message(chat_id=chat_id, text="Для возврата к выбору категории нажмите \"Назад\":",reply_markup=merchant_buttons)
    elif status == 'Battle':
        stun = user_data.get('stunned')
        if stun is None:
            bot.send_message(chat_id=chat_id, text="Вы в бою",reply_markup=get_general_battle_buttons(player))
        elif stun == 0:
            user_data.pop('stunned')
            bot.send_message(chat_id=chat_id, text="Вы в бою", reply_markup=get_general_battle_buttons(player))
    elif status == 'Info':
        print_player(bot, update, user_data)
