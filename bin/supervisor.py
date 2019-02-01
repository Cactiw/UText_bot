import datetime, time
import work_materials.globals as globals

from telegram.error import TelegramError

from work_materials.globals import *

TIME_BETWEEN_REPORTS = 10 * 60

def process_monitor(processes):
    message = dispatcher.bot.sync_send_message(chat_id = STATUS_REPORT_CHANNEL_ID, text = "started, please wait...")
    while globals.processing:
        OK = True
        response = "Status report for {0}:\n".format(datetime.datetime.now(tz=moscow_tz))
        for process in processes:
            response += "{0}{1}\n".format("✅" if process.is_alive() else "🛑", process.name)
            if not process.is_alive():
                OK = False
        workers_alive = dispatcher.bot.check_workers()
        workers_total = dispatcher.bot.num_workers
        if workers_alive != workers_total:
            OK = False
        response += "{2}{0} bot workers of {1} are alive\n".format(workers_alive, workers_total, "✅" if workers_alive == workers_total else "🛑")
        response += "\n{0}".format("❇️ Everything is OK" if OK else "‼️‼️ ALERT ‼️‼️\n@Cactiw @KhGleb")
        try:
            dispatcher.bot.editMessageText(chat_id=message.chat_id, message_id=message.message_id, text=response, parse_mode='HTML')
        except TelegramError:
            message = dispatcher.bot.sync_send_message(chat_id = STATUS_REPORT_CHANNEL_ID, text=response, parse_mode='HTML')
        if not OK:
            dispatcher.bot.sync_send_message(chat_id=ALERT_NOTIFICATIONS_CHANNEL_ID, text=response, parse_mode='HTML')
        for i in range(0, TIME_BETWEEN_REPORTS):
            time.sleep(1)
            if not globals.processing:
                break
