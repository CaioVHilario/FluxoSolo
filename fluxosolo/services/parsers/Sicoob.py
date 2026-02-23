from pathlib import Path
import pandas as pd
import numpy as np

import pdfplumber

CAMINHO_ATUAL = Path(__file__).resolve()
RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent.parent
CAMINHO_PDF = RAIZ_DO_PROJETO / "data" / "sicoob_2024_02_21_10_58_48.pdf"

all_rows = []


with pdfplumber.open(CAMINHO_PDF) as pdf:

    for page in pdf.pages:
        tables = page.extract_tables()  # extrair tabelas das paginas

        header = False  # Para pular a primeira tabela de cabeçalho do PDF

        # loop para criar um dict para cada tabela
        for table in tables:
            if table and header:
                clean_table = [row for row in table]
                # lista de todos os dataframes
                all_rows.extend(clean_table)

            header = True

if all_rows:
    # cria o dataframe para todas as tabeas extraidas do PDF
    df_extract = pd.DataFrame(all_rows)

    # nomeia colunas e preenche dados vazios com NaN
    df_extract.columns = ["Data", "Transação", "Valor_texto"]
    df_extract = df_extract.replace(r"^\s*$", np.nan, regex=True)

    # Separa resumo do extrato das transações
    filtro_resumo = df_extract["Data"].str.contains(
        "SALDO|VENCIMENTO", case=False, na=False
    )
    df_resumo = df_extract[filtro_resumo].copy()
    df_transactions = df_extract[~filtro_resumo].copy()

    # Tira linhas irrelevantes do df
    valores_para_remover = [
        "SALDO DO DIA",
        "SALDO BLOQ.ANTERIOR",
        "Transferência Pix",
        "Recebimento Pix",
        "Pagamento Pix",
    ]
    df_transactions = df_transactions[
        ~df_transactions["Transação"].isin(valores_para_remover)
    ]

    # Removendo linhas desnecessárias que contenham algumas das seguintes palavras
    palavras_a_remover = [
        "DOC\.:",
        "registro\(s\)",
        "202401",
        "REM\.:",
        "\*\*\*",
    ]
    padrao_regex = "|".join(palavras_a_remover)
    df_transactions = df_transactions[
        ~df_transactions["Transação"].str.contains(
            padrao_regex, na=False, case=False, regex=True
        )
    ]

    # Encontra linhas onde Valor contenha "\n" e remove
    df_transactions["Valor_texto"] = df_transactions[
        "Valor_texto"
    ].str.replace("\n", "", regex=False)

    # Separa valor do tipo (D ou C)
    df_transactions[["Valor", "Tipo"]] = df_transactions[
        "Valor_texto"
    ].str.extract(r"([\d.,]+)([DC])")
    df_transactions["Valor"] = (
        df_transactions["Valor"]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    df_transactions["Valor"] = np.where(
        df_transactions["Tipo"] == "D",
        df_transactions["Valor"] * -1,
        df_transactions["Valor"],
    )

    # Criando ID para cada transação e agrupa as transações
    df_transactions["Transaction_ID"] = (
        df_transactions["Data"].notna().cumsum()
    )
    df_transactions["num_linhas"] = df_transactions.groupby(
        "Transaction_ID"
    ).cumcount()

    # Remove restante das linhas com informações desnecessárias para fazer o pivot
    df_transactions = df_transactions[df_transactions["num_linhas"] <= 1]

    # Pivot do df para criar a colua "Detalhes"
    df_pivot = df_transactions.pivot(
        index="Transaction_ID", columns="num_linhas"
    )
    # Limpa colunas vazias
    df_pivot = df_pivot.dropna(axis=1, how="all")
    df_resumo = df_resumo.dropna(axis=1, how="all")

    # Renomeia as colunas
    df_pivot.columns = [
        "Data",
        "Transação",
        "Detalhes",
        "Valor_texto",
        "Valor",
        "Tipo",
    ]

    # Adicionar ano a data (isso é provisório!!!)
    df_pivot['Data'] = df_pivot['Data'] + '/2024'

    # Convertendo para datetime
    df_pivot['Data'] = pd.to_datetime(df_pivot['Data'], format='%d/%m/%Y')

    # Organizando df do resumo da fatura
    df_resumo.columns = [
        "Transação",
        "Valor",
    ]

    df_resumo = df_resumo[
        ~df_resumo["Transação"].str.contains(
            'VENCIMENTO CHEQUE', na=False, case=False
        )
    ]

    df_pivot = df_pivot.drop(['Valor_texto', 'Tipo'], axis=1)

    print(df_extract)
    print(df_pivot.to_string())
    print(df_resumo)