from pathlib import Path
import pandas as pd
import numpy as np


CAMINHO_ATUAL = Path(__file__).resolve()
RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent.parent
CAMINHO_PDF = RAIZ_DO_PROJETO / "data" / "NU_414920686_01JAN2026_31JAN2026.csv"

all_rows = []

df_nubank = pd.read_csv(CAMINHO_PDF, parse_dates=['Data'], date_format='%d/%m/%Y')

df_nubank[['Transação', 'Detalhes']] = df_nubank['Descrição'].str.split('-', expand=True, n=2).iloc[:, :2]
df_nubank = df_nubank.drop(['Identificador', 'Descrição'], axis=1)

print(df_nubank.to_string())
print(df_nubank.dtypes)
