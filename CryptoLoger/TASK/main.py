import base64
import time
import subprocess
import string
import random


def get_time():
    t = "08:46"
    # t = time.strftime("%H:%M", time.localtime())
    return base64.b64encode(t.encode()).decode()


def get_date():
    d = "11/09/2001"
    # d = time.strftime("%D", time.localtime())
    return bin(int(d.replace("/", "")))[2:].zfill(8)


def get_name():
    shift = random.randint(1, 25)
    letters = string.ascii_letters
    # n = subprocess.run("hostname", capture_output=True).stdout.decode()
    n = "JohnDoe"

    s = ""
    for i in n:
        s += letters[(letters.index(i) + shift) % len(letters)] if i in letters else ""

    return s


def get_note():
    # n = input("Enter a phrase: ")
    n = "Reboot is my tool"
    return ".".join(str(ord(c)) for c in n)


if __name__ == "__main__":
    _time = get_time()
    _date = get_date()
    _name = get_name()
    _note = get_note()

    key = f"{_time}|{_date}|{_name}|{_note}"
    print(f"{key=}")
