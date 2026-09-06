# ignore this file
""" Json generator"""

import json
import os
from pathlib import Path

data = []
l2 = [5, 9, 25, 26, 27, 28, 17, 29, 30, 31, 32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 47]
l1 = [x for x in range(2, 48) if x not in l2]
print(l1)
print(l2)
test = Path.home().joinpath("PycharmProjects/G80.2023.T3.EG03/src/Json/test/valid.json")
for i in l1:
    for j in [0, 1]:
        if j == 0:
            ADD = "delete"
        else:
            ADD = "duplicate"
        # pylint: disable=invalid-name
        file = (
            str(
                Path.home().joinpath(
                    "PycharmProjects/G80.2023.T3.EG03/src/Json/test/nodo"
                )
            )
            + str(i)
            + "_"
            + ADD
            + ".json"
        )
        if os.path.isfile(file):
            os.remove(file)
        with open(test, "r", encoding="utf8") as file1:
            data = json.load(file1)
        with open(file, "w", encoding="utf8") as file2:
            json.dump(data, file2, indent=2)

for i in l2:
    # pylint: disable=invalid-name
    file = (
        str(Path.home().joinpath("PycharmProjects/G80.2023.T3.EG03/src/Json/test/nodo"))
        + str(i)
        + "_modification.json"
    )
    test = Path.home().joinpath(
        "PycharmProjects/G80.2023.T3.EG03/src/Json/test/valid.json"
    )
    if os.path.isfile(file):
        os.remove(file)
    with open(test, "r", encoding="utf8") as file1:
        data = json.load(file1)
    with open(file, "w", encoding="utf8") as file2:
        json.dump(data, file2, indent=2)
