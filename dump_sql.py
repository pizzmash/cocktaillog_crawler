import csv


def dump(table_name, column_names, is_str, source, dump_path):
    with open(dump_path, "w") as fo:
        fo.write("INSERT INTO ")
        fo.write(table_name)
        fo.write(" (")
        fo.write(",".join(column_names + ["updatedAt"]))
        fo.write(") VALUES\n")
        with open(source) as fi:
            reader = csv.reader(fi)
            reader.__next__()
            for i, row in enumerate(reader):
                if i != 0:
                    if i % 100 != 0:
                        fo.write(",\n")
                    else:
                        fo.write(";\n\nINSERT INTO ")
                        fo.write(table_name)
                        fo.write(" (")
                        fo.write(",".join(column_names + ["updatedAt"]))
                        fo.write(") VALUES\n")
                fo.write("(")
                fo.write(
                    ",".join(
                        [
                            "'{}'".format(e.replace("'", "’"))
                            if is_str_
                            else e
                            if e != ""
                            else "null"
                            for e, is_str_ in zip(row, is_str)
                        ]
                    )
                )
                fo.write(",datetime('now', 'localtime')")
                fo.write(")")
        fo.write(";")


dump("Glass", ["id", "name"], [False, True], "data/glass.csv", "sql/glass.sql")
dump(
    "Technique",
    ["id", "name"],
    [False, True],
    "data/technique.csv",
    "sql/technique.sql",
)
dump(
    "DrinkKind",
    ["id", "name"],
    [False, True],
    "data/drink_kind.csv",
    "sql/drink_kind.sql",
)
dump(
    "Drink",
    ["id", "name", "kindId"],
    [False, True, False],
    "data/drink.csv",
    "sql/drink.sql",
)
dump(
    "Cocktail",
    ["id", "name", "description", "alcohol", "glassId", "techniqueId", "image"],
    [False, True, True, True, False, False, True],
    "data/cocktail.csv",
    "sql/cocktail.sql",
)
dump(
    "CocktailDrink",
    ["id", "cocktailId", "drinkId", "quantity"],
    [False, False, False, True],
    "data/cocktail_drink.csv",
    "sql/cocktail_drink.sql",
)
