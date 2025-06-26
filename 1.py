import base64

with open("1.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    line = base64.b64decode(line.encode("utf-8")).decode("utf-8").replace("*", "")
    if "flag" in line:
        print(line)
