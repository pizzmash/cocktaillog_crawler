import csv


kinds_dict = {}

with open("data/drink_kinds.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        kinds_dict[row["name"]] = row["id"]

drinks = []

with open("data/drink.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        drinks.append([row["id"], row["name"]])

for drink in drinks:
    if drink[1] in kinds_dict:
        drink.append(kinds_dict[drink[1]])
    else:
        drink.append("")

with open("data/drink.csv", "w") as f:
    fieldnames = ["id", "name", "kind_id"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for drink in drinks:
        writer.writerow({"id": drink[0], "name": drink[1], "kind_id": drink[2]})
