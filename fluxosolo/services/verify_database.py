import pandas as pd
import sqlalchemy.exc as OperationalError
import streamlit as st


def verify_database(df: pd.DataFrame):

    conn = st.connection("sql")

    params = {
        "init": str(df["date"].min()),
        "end": str(df["date"].max()),
        "bank": str(df["bank"].min()),
    }

    query_verification_extract = """
        SELECT COUNT(*) as 'total' FROM transactions
        WHERE date BETWEEN :init AND :end
        AND bank = :bank
    """

    try:
        df_check = conn.query(query_verification_extract, params=params, ttl=0)
        return int(df_check["total"].iloc[0])

    except OperationalError:
        return 0
