import work_materials.globals
from work_materials.globals import *
import time, pickle

def loadData():
    try:
        f = open('backup/userdata', 'rb')
        dispatcher.user_data = pickle.load(f)
        f.close()
        print("Data picked up")
    except FileNotFoundError:
        work_materials.globals.logging.error("Data file not found")
    except:
        work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])


def saveData():
    global processing
    try:
        exit = 0
        while work_materials.globals.processing and exit == 0:
            for i in range(0, 6):
                time.sleep(5)
                if work_materials.globals.processing == 0:
                        exit = 1
                        break
            # Before pickling
            print("Writing data, do not shutdown bot...")

            try:
                to_dump = {}
                for i in travel_jobs:
                    j = travel_jobs.get(i)
                    to_dump.update({i: [j.get_time_spent(), j.get_time_left()]})

                f = open('backup/userdata', 'wb+')
                pickle.dump(dispatcher.user_data, f)
                f.close()
                f = open('backup/travel_jobs', 'wb+')
                pickle.dump(to_dump, f)
                f.close()
                print("Data write completed")
            except:
                work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])
    except KeyboardInterrupt:
        print("Writing data last time, do not shutdown bot...")
        try:
            f = open('backup/userdata', 'wb+')
            pickle.dump(dispatcher.user_data, f)
            f.close()
            f = open('backup/travel_jobs', 'wb+')
            pickle.dump(to_dump, f)
            f.close()
            print("Data write completed")
        except:
            work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])
        return
