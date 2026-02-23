import pandas as pd

from Base import BaseParser

class NubankParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath):
        #Lê arquivo csv
        df_nubank = pd.read_csv(filepath, parse_dates=['Data'], date_format='%d/%m/%Y', encoding=self.encoding)

        #austa colunas e renomeias
        df_nubank[['Transação', 'Detalhes']] = df_nubank['Descrição'].str.split('-', expand=True, n=2).iloc[:, :2]
        df_nubank = df_nubank.drop(['Identificador', 'Descrição'], axis=1)
        df_nubank = df_nubank[['Data', 'Transação', 'Detalhes', 'Valor']]

        #print(df_nubank.to_string())
        #print(df_nubank.dtypes)

        return df_nubank
