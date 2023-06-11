class Table:
    def __init__(self, table_name, filed_names, search_column_idx=None):
        self.table_name = table_name
        self.field_names = filed_names
        self.table = []
        self.search_column_idx = search_column_idx
        self.search_column_set = set()
        self.next_id = 0

    def add(self, item):
        self.table.append(item)
        if (
            self.search_column_idx is not None
            and item[self.search_column_idx] not in self.search_column_set
        ):
            self.search_column_set |= {item[self.search_column_idx]}

    def idx_of(self, search_comlmn_value):
        if (
            self.search_column_idx is not None
            and search_comlmn_value in self.search_column_set
        ):
            return [item[self.search_column_idx] for item in self.table].index(
                search_comlmn_value
            )
        else:
            return None

    def __len__(self):
        return len(self.table)
