from pathlib import Path
import pandas as pd
import numpy as np

import pdfplumber

CAMINHO_ATUAL = Path(__file__).resolve()
RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent
CAMINHO_PDF = RAIZ_DO_PROJETO/'data'/'sicoob_2024_02_21_10_58_48.pdf'

list_of_dfs = []


with pdfplumber.open(CAMINHO_PDF) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables() #extrair tabelas das paginas

        #loop para criar um dataframe para cada tabela
        for table in tables:

            if table:
                df_temp = pd.DataFrame(table)
                #lista de todos os dataframes
                list_of_dfs.append(df_temp)

if list_of_dfs:
    #concatena todos os dataframes em um só
    df_final = pd.concat(list_of_dfs, ignore_index=True)
    print(df_final)
