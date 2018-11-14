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
        while work_materials.globals.processing:
            time.sleep(30)
            # Before pickling
            print("Writing data, do not shutdown bot...")
            try:
                f = open('backup/userdata', 'wb+')
                pickle.dump(dispatcher.user_data, f)
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
            print("Data write completed")
        except:
            work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])
        return
