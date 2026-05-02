import pandas as pd

from fluxosolo.core.database import engine


def read_id_and_name_from_table(table):
    return pd.read_sql(f"SELECT id, name FROM {table};", con=engine)
