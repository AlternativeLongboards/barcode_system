import time
from pymongo import MongoClient


#client = MongoClient('mongodb://213.32.89.50:27017/')
client = MongoClient('mongodb://192.168.1.200:27017/')

db = client['production']
staff = db['staff']
collection_00 = db['preparing']
collection_01 = db['pressing']
collection_02 = db['cutting']
collection_03 = db['sanding']
collection_04 = db['finishing']
topress = db['topress']
tocut = db['tocut']
tosand = db['tosand']
tofinish = db['tofinish']
stock = db['stock']
evermade = db['evermade']
time.sleep(3)


def remove_record():

    print('0 dla 00 - LAGGING')
    print('1 dla 01 - PRESSING')
    print('2 dla 02 - CUTTING')
    print('3 dla 03 - SANDING')
    print('4 dla 04 - FINISHING')

    choice = input('Wybierz kategorie')

    if (choice == "0") or (choice == "1") or (choice == "2") or (choice == "3") or (choice == "4"):

        code = input('Wpisz numer kodu kreskowego BEZ OSTATNIEGO NUMERU')

        if (len(code) == 13):
            print('KOD ZA DLUGI')

        if (len(code) == 12):

            if (choice == "0"):

                result = collection_00.delete_many({"code": code})
                if (result.deleted_count > 0):
                    print('USUNIĘTO Z BAZY 00')
                    results2 = topress.delete_many({"code": code})
                    if (results2.deleted_count > 0):
                        print('USUNIETO Z BAZY TO_PRESS')
                else:
                    print('NIE BYLO W BAZIE 00')

            if (choice == "1"):

                result = collection_01.delete_many({"code": code})
                if (result.deleted_count > 0):
                    print('USUNIĘTO Z BAZY 01')
                    results2 = tocut.delete_many({"code": code})
                    if (results2.deleted_count > 0):
                        print('USUNIETO Z BAZY TO_CUT')
                else:
                    print('NIE BYLO W BAZIE 01')

            if (choice == "2"):

                result = collection_02.delete_many({"code": code})
                if (result.deleted_count > 0):
                    print('USUNIĘTO Z BAZY 02')
                    results2 = tosand.delete_many({"code": code})
                    if (results2.deleted_count > 0):
                        print('USUNIETO Z BAZY TO_SAND')
                else:
                    print('NIE BYLO W BAZIE 02')

            if (choice == "3"):

                result = collection_03.delete_many({"code": code})
                if (result.deleted_count > 0):
                    print('USUNIĘTO Z BAZY 03')
                    results2 = tofinish.delete_many({"code": code})
                    if (results2.deleted_count > 0):
                        print('USUNIETO Z BAZY TO_FINISH')
                else:
                    print('NIE BYLO W BAZIE 03')

            if (choice == "4"):

                result = collection_04.delete_many({"code": code})
                if (result.deleted_count > 0):
                    print('USUNIĘTO Z BAZY 04')
                    results2 = stock.delete_many({"code": code})
                    if (results2.deleted_count > 0):
                        print('USUNIETO Z BAZY STOCK')
                    result3 = evermade.delete_many({"code": code})
                    if (result3.deleted_count > 0):
                        print('USUNIETO Z BAZY EVERMADE')
                else:
                    print('NIE BYLO W BAZIE 04')

    else:
        print('Zły wybór')

remove_record()
