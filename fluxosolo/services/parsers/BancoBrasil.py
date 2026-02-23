from pathlib import Path
import pandas as pd
import numpy as np

from Base import BaseParser

CAMINHO_ATUAL = Path(__file__).resolve()
RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent.parent
CAMINHO_PDF = RAIZ_DO_PROJETO / "data" / "Extrato conta corrente - 012026.csv"

class BancoBrasiParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath):
        
        all_rows = []

        # Leo csv e armazena em dataframe
        df_bancoBrasil = pd.read_csv(CAMINHO_PDF, encoding=self.encoding, parse_dates=['Data'], date_format='%d/%m/%Y')

        # Renomeia as colunas do dataframe para nomes com caracteres normais e tira 
        # a coluna 'N documento'
        df_bancoBrasil.columns = [
            "Data",
            "Transação",
            "Detalhes",
            "N documento",
            "Valor",
            "Tipo Lançamento"

        ]
        df_bancoBrasil = df_bancoBrasil.drop(['N documento'], axis=1)
        df_bancoBrasil = df_bancoBrasil.drop(['Tipo Lançamento'], axis=1)

        # Tira linhas que não são referentes a entradas e saidas do extrato
        lancamentos_a_remover = ['Saldo do dia', 'Saldo Anterior']
        df_bancoBrasil = df_bancoBrasil[
            ~df_bancoBrasil['Transação'].isin(lancamentos_a_remover)
        ]

        #Altera virgula por ponto e converte o tipo do valor pra float
        df_bancoBrasil['Valor'] = df_bancoBrasil['Valor'].str.replace(',', '.', regex=False)
        df_bancoBrasil['Valor'] = df_bancoBrasil['Valor'].astype(float)

        df_bancoBrasil['Data'] = pd.to_datetime(df_bancoBrasil['Data'], format='%d/%m/%Y')

        #Separa o dataframe com o saldo atual da conta  e extrato
        filtro_saldo = df_bancoBrasil['Transação'].str.contains(
            'S A L D O',
            case=False, 
            na=False
        )
        df_saldo = df_bancoBrasil[filtro_saldo].copy()
        df_bancoBrasil = df_bancoBrasil[~filtro_saldo].copy()

        #limpa datafram de saldo
        df_saldo = df_saldo.drop(['Detalhes'], axis=1)

        #print(df_bancoBrasil.to_string())
        #print(df_saldo.to_string())
        #print(df_bancoBrasil.dtypes)

        return df_bancoBrasil
