from work_materials.buttons.battle_buttons import get_allies_buttons, get_enemies_buttons, get_all_targets_buttons
from work_materials.globals import pending_battles


def get_battle(battle_id):
    return pending_battles.get(battle_id)


def choose_enemy_target(bot, update, user_data):
    #Сохранить в user_data скилл, который выбрал игрок
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель", reply_markup=get_enemies_buttons(get_battle(user_data.get('Battle id')), user_data.get('Team')))
    user_data.update({'status': 'Choosing target'})


def choose_friendly_target(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель", reply_markup=get_allies_buttons(get_battle(user_data.get('Battle id')), user_data.get('Team')))
    user_data.update({'status': 'Choosing target'})


def choose_any_target(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель", reply_markup=get_all_targets_buttons(get_battle(user_data.get('Battle id')), user_data.get('Team')))
    user_data.update({'status': 'Choosing target'})


#skill == 0 => пропуск хода
#target == 0 => на себя

def battle_count():     #Тут считается битва в которой все выбрали действие, отдельный процесс
    pass
