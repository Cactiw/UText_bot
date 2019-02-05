from work_materials.globals import pending_battles, dispatcher
from bin.player_service import get_player, update_status
from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue
from bin.show_general_buttons import show_general_buttons


def status_monitor():
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
            list_user_data = list(user_data)
            if 'saved_battle_status' in list_user_data:
                user_data.pop('saved_battle_status')
            if 'chosen skill' in list_user_data:
                user_data.pop('chosen skill')
            if 'Battle waiting update' in list_user_data:
                user_data.pop('Battle waiting update')
            if 'Battle id' in list_user_data:
                user_data.pop('Battle id')
            if 'matchmaking' in list_user_data:
                user_data.pop('matchmaking')
            if 'Team' in list_user_data:
                user_data.pop('Team')
            if 'Test' in list_user_data:
                user_data.pop('Test')
            player = get_player(data.id)
            player.saved_battle_status = None

        data = interprocess_queue.get()
    return 0
