import work_materials.globals as globals
from work_materials.globals import *

def sql(bot, update, user_data):
    mes = update.message
    request = mes.text.partition(" ")[2]
    try:
        cursor.execute(request)
    except:
        response = str(sys.exc_info()[0])
        bot.send_message(chat_id=mes.from_user.id, text=response)
        return
    conn.commit()
    row = cursor.fetchone()
    response = ""
    while row:
        for i in range(0, len(row)):
            response += str(row[i]) + " "
        row = cursor.fetchone()
        response += "\n\n"
    bot.send_message(chat_id=mes.from_user.id, text=response)
