import csv
import os


class TableCsvWriter:
    @classmethod
    def write(cls, table, dir):
        with open(os.path.join(dir, table.table_name + ".csv"), mode="w") as f:
            writer = csv.DictWriter(f, fieldnames=["id"] + table.field_names)

            writer.writeheader()
            for id, item in enumerate(table.table):
                item_dict = {fn: v for fn, v in zip(table.field_names, item)}
                item_dict["id"] = id
                writer.writerow(item_dict)
