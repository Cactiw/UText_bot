from bin.player_service import update_status, get_player
from bin.battle_pve_start import battle_pve_start
from libs.enemies import AIDSEnemy

def farm(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    bot.send_message(chat_id = update.message.chat_id, text="Вы отправились фармить")
    update_status("farming", player, user_data)
    battle_pve_start([player], [AIDSEnemy(1),])
