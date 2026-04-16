import pandas as pd

from fluxosolo.core.database import engine
from fluxosolo.services.read_db import read_id_and_name_from_table
from fluxosolo.services.transform_df import (
    df_with_new_values, add_fk_id_column
)


def persist_on_db(df: pd.DataFrame):
    # Garante que a data está em datetime no dataframe
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    print("Colocando dados no banco de dados...")

    df_transaction = df.rename(columns={
        'category': 'category_id',
        'transaction_type': 'transaction_type_id',
        'bank': 'bank_id'
    })

    dict_tables = {
        'category': 'categories',
        'transaction_type': 'transactions_type',
        'bank': 'banks'
    }

    for key, value in dict_tables.items():
        df_sql = read_id_and_name_from_table(value)

        df_table = df_with_new_values(df, key, df_sql)
        
        if df_table is not None:
            df_table.to_sql(
                value,
                con=engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=500
            )

        df_transaction[f'{key}_id'] = add_fk_id_column(
            df_transaction, df_sql, f'{key}_id'
        )

    # TEMPORARIO - Será removido, apenas para salvar no banco enquanto não crio 
    # authenticação de usuarios
    df_transaction['user_id'] = 1

    # Armazena o dataframe no banco de dados
    df_transaction.to_sql(
        "transactions",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )
    print("Ação concluida!")
