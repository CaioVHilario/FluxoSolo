import pandas as pd
import streamlit as st


def verify_database(df: pd.DataFrame):

    conn = st.connection('sql')

    init_date = df['date'].min()
    end_date = df['date'].max()
    bank = df['bank'].min()

    query_verification_extract = """
        SELECT COUNT(*) as 'total' FROM transactions
        WHERE date BETWEEN :init AND :end
        AND bank = :bank
    """

    try: 

        df_check = conn.query(
            query_verification_extract,
            params={
                'init': str(init_date), 
                'end': str(end_date), 
                'bank': str(bank)
            },
            ttl=0
        )
        qtd_exists = df_check['total'].iloc[0]
    
    except Exception:

        qtd_exists = 0
    
    return qtd_exists