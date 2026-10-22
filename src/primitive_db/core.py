def create_table(metadata, table_name, columns):
    metadata[table_name] = ["ID:int"] + columns
    return metadata