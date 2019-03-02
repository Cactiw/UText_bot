from bin.player_service import update_status, get_player
from bin.battle_pve_start import battle_pve_start
from libs.enemies import AIDSEnemy

def farm(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    bot.send_message(chat_id = update.message.chat_id, text="Вы отправились фармить")
    update_status("farming", player, user_data)
    battle_group = user_data.get("battle_group")
    if battle_group is not None:
        if update.message.from_user.id != battle_group.creator:
            bot.send_message(chat_id = update.message.from_user.id, text = "Только лидер группы может отправляться фармить!")
            return
        battle_list = []
        for player_id in battle_group.players:
            curr_player = get_player(player_id)
            battle_list.append(curr_player)
    else:
        battle_list = [player]
    battle_pve_start(battle_list, [AIDSEnemy(1),])
