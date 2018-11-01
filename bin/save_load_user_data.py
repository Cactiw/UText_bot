import work_materials.globals
import time, pickle

def loadData():
    try:
        f = open('backup/userdata', 'rb')
        work_materials.globals.dispatcher.user_data = pickle.load(f)
        f.close()
        print("Data picked up")
    except FileNotFoundError:
        work_materials.globals.logging.error("Data file not found")
    except:
        work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])

def saveData():
    global processing
    try:
        while True:
            time.sleep(30)
            # Before pickling
            print("Writing data, do not shutdown bot...")
            try:
                f = open('backup/userdata', 'wb+')
                pickle.dump(work_materials.globals.dispatcher.user_data, f)
                f.close()
                print("Data write completed")
            except:
                work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])
    except KeyboardInterrupt:
        print("Writing data, do not shutdown bot...")
        try:
            f = open('backup/userdata', 'wb+')
            pickle.dump(work_materials.globals.dispatcher.user_data, f)
            f.close()
            print("Data write completed")
        except:
            work_materials.globals.logging.error(work_materials.globals.sys.exc_info()[0])
        return
