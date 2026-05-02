def df_with_new_values(df, column_table, df_sql):

    df = df[[column_table]].drop_duplicates()
    df = df.rename(columns={column_table: "name"})
    return df[~df["name"].isin(df_sql["name"])]


def add_fk_id_column(df_transaction, df_sql, fk_column):

    map_id = df_sql.set_index("name")["id"].to_dict()
    return df_transaction[fk_column].map(map_id)
