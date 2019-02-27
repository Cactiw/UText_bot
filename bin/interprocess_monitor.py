from work_materials.globals import pending_battles, dispatcher, players_need_update
from bin.player_service import get_player, update_status
from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue
from bin.show_general_buttons import show_general_buttons


def interprocess_monitor():
    data = interprocess_queue.get()
    while data is not None:
        keys = list(data.data.keys())
        if data.type == "user_data":
            user_data = dispatcher.user_data.get(data.id)
            player = get_player(data.id)
            if 'status' in keys:
                update_status(data.data.get('status'), player, user_data)
                data.data.pop('status')
                keys.remove('status')
            for user_data_record in keys:
                user_data.update({ user_data_record : data.data.get(user_data_record)})
        elif data.type == "battles_pending":
            for record in keys:
                pending_battles.update({ record: data.data.get(record)})
        elif data.type == "battle status return":
            dispatcher.user_data.get(data.id).update({'status': dispatcher.user_data.get(data.id).get('saved_battle_status')})
            user_data = dispatcher.user_data.get(data.id)
            if user_data.get('status') == None:
                dispatcher.user_data.get(data.id).update({'status': 'In Location'})
            list_user_data = list(user_data)
            if 'saved_battle_status' in list_user_data:
                user_data.pop('saved_battle_status')
            if 'chosen skill' in list_user_data:
                user_data.pop('chosen skill')
            if 'Battle_waiting_to_count' in list_user_data:
                user_data.pop('Battle_waiting_to_count')
            if 'Battle id' in list_user_data:
                try:
                    pending_battles.pop(user_data.get('Battle id'))
                except KeyError:
                    pass
                user_data.pop('Battle id')
            if 'matchmaking' in list_user_data:
                user_data.pop('matchmaking')
            if 'Team' in list_user_data:
                user_data.pop('Team')
            if 'stunned' in list_user_data:
                user_data.pop('stunned')
            if 'Test' in list_user_data:
                user_data.pop('Test')
            player = get_player(data.id)
            player.saved_battle_status = None
            show_general_buttons(dispatcher.bot, player.id, user_data)
        elif data.type == "remove stun":
            user_data = dispatcher.user_data.get(data.id)
            list_user_data = list(user_data)
            if "stunned" in list_user_data:
                user_data.pop('stunned')
        elif data.type == "change_player_state":
            player = get_player(data.data[0])
            list_keys = list(data.data[1:])
            for key in list_keys:
                change_value = data.data.get(key)
                if key == "exp":
                    player.exp += change_value
                    player.lvl_check()
                elif key == "dead":
                    player.dead = change_value
                elif key == "resources":
                    for new_key in change_value:
                        delta = change_value.get(new_key)
                        old_value = player.resourses.get(new_key)
                        if old_value is None:
                            continue
                        old_value += delta
                        player.resources.update({new_key : old_value})
                elif key == "eq_backpack":
                    for new_key in change_value:
                        delta = change_value.get(new_key)
                        old_value = player.eq_backpack.get(new_key)
                        if old_value is None:
                            continue
                        old_value += delta
                        player.resources.update({new_key : old_value})
                elif key == "al_backpack":
                    for new_key in change_value:
                        delta = change_value.get(new_key)
                        old_value = player.al_backpack.get(new_key)
                        if old_value is None:
                            continue
                        old_value += delta
                        player.resources.update({new_key : old_value})    
                elif key == "res_backpack":
                    for new_key in change_value:
                        delta = change_value.get(new_key)
                        old_value = player.res_backpack.get(new_key)
                        if old_value is None:
                            continue
                        old_value += delta
                        player.resources.update({new_key : old_value})
                players_need_update.put(player)
        data = interprocess_queue.get()
    return 0
