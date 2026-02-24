import pandas as pd

from fluxosolo.services.parsers.Base import BaseParser

class NubankParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath: str) -> pd.DataFrame:
        #Lê arquivo csv
        df_nubank = pd.read_csv(filepath, parse_dates=['Data'], date_format='%d/%m/%Y', encoding=self.encoding)

        #austa colunas e renomeias
        df_nubank[['Transação', 'Detalhes']] = df_nubank['Descrição'].str.split('-', expand=True, n=2).iloc[:, :2]
        df_nubank = df_nubank.drop(['Identificador', 'Descrição'], axis=1)

        map_rename = {
            'Data': 'date',
            'Transação': 'transaction',
            'Detalhes': 'details',
            'Valor': 'value'
        }

        df_nubank = df_nubank.rename(columns=map_rename)

        df_nubank['bank'] = 'NuBank'

        #print(df_nubank.to_string())
        #print(df_nubank.dtypes)

        return df_nubank
