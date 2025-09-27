import os

lockey = None

def lock(key):
    global lockey
    if os.path.exists("encode.lock"):
        return False
    else:
        lockey = key
        open("encode.lock", "w").write("lock")
        return True

def is_locked():
    return os.path.exists("encode.lock")

def rmlock(key):
    global lockey
    if key == lockey:
        try:
            os.remove("encode.lock")
            lockey = None
            return True
        except:
            return False
    return False