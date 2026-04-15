import pandas as pd

from fluxosolo.core.database import engine
from fluxosolo.services.transform_df import (
    df_with_new_values, add_fk_id_column
)


def save_tables(df, table):

    if df is not None:
        df.to_sql(
            f"{table}",
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500
        )

def persist_on_db(df: pd.DataFrame):
    # Garante que a data está em datetime no dataframe
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    print("Colocando dados no banco de dados...")

    df_category = df_with_new_values(df, 'category', 'categories')
    df_transaction_type = df_with_new_values(
        df, 'transaction', 'transactions_type'
    )
    df_bank = df_with_new_values(df, 'bank', 'banks')

    save_tables(df_category, 'categories')
    save_tables(df_transaction_type, 'transactions_type')
    save_tables(df_bank, 'banks')

    df_transaction = df.rename(
        columns={
            'category': 'category_id',
            'transaction': 'transaction_type_id',
            'bank': 'bank_id'
        }
    )

    df_transaction['category_id'] = add_fk_id_column(
        df_transaction, 'categories', 'category_id'
    )
    df_transaction['transaction_type_id'] = add_fk_id_column(
        df_transaction, 'transactions_type', 'transaction_type_id'
    )
    df_transaction['bank_id'] = add_fk_id_column(
        df_transaction, 'banks', 'bank_id'
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
