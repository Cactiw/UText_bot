from work_materials.globals import *
from bin.player_service import get_player, update_status
from libs.status_interprocess import *

def status_monitor():
    data = statuses.get()
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
        data = statuses.get()
    return 0
