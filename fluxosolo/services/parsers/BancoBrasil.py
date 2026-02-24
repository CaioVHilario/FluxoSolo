from pathlib import Path
import pandas as pd
import numpy as np

from fluxosolo.services.parsers.Base import BaseParser

CAMINHO_ATUAL = Path(__file__).resolve()
RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent.parent
CAMINHO_PDF = RAIZ_DO_PROJETO / "data" / "Extrato conta corrente - 012026.csv"

class BancoBrasiParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath: str) -> pd.DataFrame:
        
        all_rows = []

        # Leo csv e armazena em dataframe
        df_bancoBrasil = pd.read_csv(filepath, encoding=self.encoding, parse_dates=['Data'], date_format='%d/%m/%Y')

        # Renomeia as colunas do dataframe para nomes com caracteres normais e tira 
        # a coluna 'N documento'
        df_bancoBrasil.columns = [
            "date",
            "transaction",
            "details",
            "document",
            "value",
            "type"
        ]
        df_bancoBrasil = df_bancoBrasil.drop(['document'], axis=1)
        df_bancoBrasil = df_bancoBrasil.drop(['type'], axis=1)

        # Tira linhas que não são referentes a entradas e saidas do extrato
        lancamentos_a_remover = ['Saldo do dia', 'Saldo Anterior']
        df_bancoBrasil = df_bancoBrasil[
            ~df_bancoBrasil['transaction'].isin(lancamentos_a_remover)
        ]

        #Altera virgula por ponto e converte o tipo do valor pra float
        df_bancoBrasil['value'] = df_bancoBrasil['value'].str.replace(',', '.', regex=False)
        df_bancoBrasil['value'] = df_bancoBrasil['value'].astype(float)

        df_bancoBrasil['date'] = pd.to_datetime(df_bancoBrasil['date'], format='%d/%m/%Y')

        #Separa o dataframe com o saldo atual da conta  e extrato
        filtro_saldo = df_bancoBrasil['transaction'].str.contains(
            'S A L D O',
            case=False, 
            na=False
        )
        df_saldo = df_bancoBrasil[filtro_saldo].copy()
        df_bancoBrasil = df_bancoBrasil[~filtro_saldo].copy()

        #limpa datafram de saldo
        df_saldo = df_saldo.drop(['details'], axis=1)

        df_bancoBrasil['bank'] = 'Banco do Brasil'

        #print(df_bancoBrasil.to_string())
        #print(df_saldo.to_string())
        #print(df_bancoBrasil.dtypes)

        return df_bancoBrasil
