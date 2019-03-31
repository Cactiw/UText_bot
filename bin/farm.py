from bin.player_service import update_status, get_player
from bin.battle_pve_start import battle_pve_start
from libs.enemies import AIDSEnemy
from work_materials.globals import grinding_players, dispatcher
import work_materials.globals as globals
from libs.random_encounters import DropEncounter
from bin.item_service import get_item

import time
import logging
import random


def fatigue_count(time_passed):
    time_passed /= 60
    print("time_passed = {}".format(time_passed))
    fatigue = int(time_passed*time_passed*time_passed/58320)
    return fatigue if fatigue <= 100 else 100


def drop_rate_percents(fatigue):
    return (-0.35 * fatigue) + 50


def farm(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    bot.send_message(chat_id=update.message.chat_id, text="Вы отправились фармить")
    update_status("farming", player, user_data)
    print(player.status)
    user_data.update({'farming_started': time.time()})
    player.grind_started_time = time.time()
    grinding_players.append(player)


def farm_monitor():
    while globals.processing:
        print(grinding_players)
        for player in grinding_players:
            print("checking grind for player {}".format(player.id))
            print(player.status)
            user_data = dispatcher.user_data.get(player.id)
            status = user_data.get('status')
            if status == "farming":
                try:
                    player.fatigue = fatigue_count(player.grind_started_time)
                except AttributeError:
                    user_data = dispatcher.user_data.get(player.id)
                    if not user_data:
                        continue
                    player.fatigue = fatigue_count(time.time() - user_data.get('farming_started'))
                print(player.fatigue)
                if player.fatigue is None:
                    logging.warning("fatigue {} is None, possible an error".format(player.id))
                # Кидаю кубик
                r = random.randint(1, 100)
                print(r, drop_rate_percents(player.fatigue), player.fatigue)
                if r <= drop_rate_percents(player.fatigue):
                    # Событие ебать
                    print("encounter happens")
                    enc = DropEncounter('Usual', 'Поздравляем, вы нашли грибы!', [get_item('r', 1)], None)
                    enc.run(player)
        for i in range(20):
            if not globals.processing:
                return 0
            time.sleep(1)


def pve_start(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    battle_group = user_data.get("battle_group")
    if battle_group is not None:
        if update.message.from_user.id != battle_group.creator:
            bot.send_message(chat_id=update.message.from_user.id, text="Только лидер группы может отправляться фармить!")
            return
        battle_list = []
        for player_id in battle_group.players:
            curr_player = get_player(player_id)
            battle_list.append(curr_player)
    else:
        battle_list = [player]
    battle_pve_start(battle_list, [AIDSEnemy(1), ])
