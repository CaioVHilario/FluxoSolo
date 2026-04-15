from fluxosolo.services.read_db import read_id_and_name_from_table


def df_with_new_values(df, column_table, table):

    df = df[[column_table]].drop_duplicates()
    df = df.rename(columns={column_table: 'name'})
    df_db = read_id_and_name_from_table(table)
    df = df[
        ~df['name'].isin(df_db['name'])
    ]

    return df
    

def add_fk_id_column(df_transaction, table, fk_column):

    df_id = read_id_and_name_from_table(table)
    map_id = df_id.set_index('name')['id'].to_dict()

    return df_transaction[fk_column].replace(map_id)