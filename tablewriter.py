class TableCsvWriter:
    @classmethod
    def write(cls, table, path):
        print("TABLE: {}".format(table.table_name))
        for i, field_name in enumerate(table.field_names):
            if i == len(table.field_names) - 1:
                print(field_name)
            else:
                print(field_name, end="\t")

        for row in table.table:
            for i, col in enumerate(row):
                if i == len(row) - 1:
                    print(col)
                else:
                    print(col, end="\t")
