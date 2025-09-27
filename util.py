import os

included = ["drive.py", "lock_unit.py", "main.py", "torrent.py", "util.py", "encode_module.py", "tmp"]

def find_addt_f():
    ld = os.listdir()

    for i in ld:
        if not i in included:
            try:
                for _ in os.listdir(i):
                    if _.endswith(".mkv"):
                        return i + "\\" + _
            except:pass
def find_addt_s():
    ld = os.listdir()
    return [i for i in ld if not i in included]