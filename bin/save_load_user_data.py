import work_materials.globals
from bin.player_service import get_player
from work_materials.globals import pending_battles, grinding_players
import time, pickle
import logging, traceback


def loadData():
    try:
        f = open('backup/userdata', 'rb')
        work_materials.globals.dispatcher.user_data = pickle.load(f)
        f.close()
        f = open('backup/battles', 'rb')
        pending_battles_tmp = pickle.load(f)
        for i in list(pending_battles_tmp):
            battle = pending_battles_tmp.get(i)
            battle.last_count_time = time.time()
            pending_battles.update({i: battle})
        f.close()
        f = open('backup/grinding_players', 'rb')
        grinding_players_ids = pickle.load(f)
        for player_id in grinding_players_ids:
            player = get_player(player_id)
            grinding_players.append(player)
        print("Data picked up")
    except FileNotFoundError:
        logging.error("Data file not found")
    except:
        logging.error(traceback.format_exc())


def saveData():
    global processing
    try:
        exit = 0
        while exit == 0:
            for i in range(0, 5):
                time.sleep(5)
                if work_materials.globals.processing == 0:
                        exit = 1
                        break
            # Before pickling
            logging.debug("Writing data, do not shutdown bot...\r")
            if exit:
                logging.warning("Writing data last time, do not shutdown bot...")

            try:
                to_dump = {}
                for i in work_materials.globals.travel_jobs:
                    j = work_materials.globals.travel_jobs.get(i)
                    to_dump.update({i: [j.get_time_spent(), j.get_time_left()]})
                grinding_players_ids = []
                for player in grinding_players:
                    grinding_players_ids.append(player.id)

                f = open('backup/userdata', 'wb+')
                pickle.dump(work_materials.globals.dispatcher.user_data, f)
                f.close()
                f = open('backup/travel_jobs', 'wb+')
                pickle.dump(to_dump, f)
                f.close()
                f = open('backup/battles', 'wb+')
                pickle.dump(pending_battles, f)
                f.close()
                f = open('backup/grinding_players', 'wb+')
                pickle.dump(grinding_players_ids, f)
                f.close()
                logging.debug("Data write completed\b")
            except Exception:
                logging.error(traceback.format_exc())
    except KeyboardInterrupt:
        print("Writing data last time, do not shutdown bot...")
        try:
            f = open('backup/userdata', 'wb+')
            pickle.dump(work_materials.globals.dispatcher.user_data, f)
            f.close()
            f = open('backup/travel_jobs', 'wb+')
            pickle.dump(to_dump, f)
            f.close()
            print("Data write completed")
        except Exception:
            logging.error(traceback.format_exc())
        return
