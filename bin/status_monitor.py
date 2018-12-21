from work_materials.globals import *
from bin.player_service import get_player, update_status
from libs.status_interprocess import *

def status_monitor():
    data = statuses.get()
    while data is not None:
        user_data = dispatcher.user_data.get(data.id)
        player = get_player(data.id)
        update_status(data.new_status, player, user_data)
        data = statuses.get()
    return 0