import threading
import os

lock = threading.Lock()

FILENAME = "door.state"


def is_closed():
    return "closed" == read_state()

def is_open():
    return "open" == read_state()


def write_state(state):
    with lock:
        with open(FILENAME, 'w') as f:
            f.write(state)

def read_state():
    if os.exists(FILENAME):
        with lock:
            with open(FILENAME, 'r') as f:
                return f.read()
    else:
        write_state("closed")
