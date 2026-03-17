import pandas as pd

from fluxosolo.core.database import engine


def save_extract(df: pd.DataFrame):
    # Garante que a data está em datetime no dataframe
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    print("Colocando dados no banco de dados...")

    # armazena o dataframe no banco de dados
    df.to_sql(
        "transactions",
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500,
    )
    print("Ação concluida!")
