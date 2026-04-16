import pandas as pd

from fluxosolo.services.parsers.Base import BaseParser

# CAMINHO_ATUAL = Path(__file__).resolve()
# RAIZ_DO_PROJETO = CAMINHO_ATUAL.parent.parent.parent
# filepath = RAIZ_DO_PROJETO / "data" / "Extrato conta corrente - 082023.csv"


class BancoBrasiParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath: str) -> pd.DataFrame:

        # Leo csv e armazena em dataframe
        # df_bancoBrasil = pd.read_csv(filepath, encoding=self.encoding, parse_dates=['Data'], date_format='%d/%m/%Y')
        df_bancoBrasil = pd.read_csv(
            filepath,
            encoding="latin-1",
            parse_dates=["Data"],
            date_format="%d/%m/%Y",
        )

        # Renomeia as colunas do dataframe para nomes com caracteres normais 
        # e tira a coluna 'N documento'
        df_bancoBrasil.columns = [
            "date",
            "transaction_type",
            "details",
            "document",
            "value",
            "type",
        ]
        df_bancoBrasil = df_bancoBrasil.drop(["document"], axis=1)
        df_bancoBrasil = df_bancoBrasil.drop(["type"], axis=1)

        # Tira linhas que não são referentes a entradas e saidas do extrato
        lancamentos_a_remover = ["Saldo do dia", "Saldo Anterior"]
        df_bancoBrasil = df_bancoBrasil[
            ~df_bancoBrasil["transaction_type"].isin(lancamentos_a_remover)
        ]

        # Altera virgula por ponto e converte o tipo do valor pra float
        df_bancoBrasil["value"] = df_bancoBrasil["value"].str.replace(
            ".", "", regex=False
        )
        df_bancoBrasil["value"] = df_bancoBrasil["value"].str.replace(
            ",", ".", regex=False
        )
        df_bancoBrasil["value"] = df_bancoBrasil["value"].astype(float)

        df_bancoBrasil["date"] = pd.to_datetime(
            df_bancoBrasil["date"], format="%d/%m/%Y"
        )

        # Separa o dataframe com o saldo atual da conta  e extrato
        filtro_saldo = df_bancoBrasil["transaction_type"].str.contains(
            "S A L D O", case=False, na=False
        )
        df_saldo = df_bancoBrasil[filtro_saldo].copy()
        df_bancoBrasil = df_bancoBrasil[~filtro_saldo].copy()

        # limpa datafram de saldo
        df_saldo = df_saldo.drop(["details"], axis=1)

        # Renomeia transações para padronizar com os outros bancos
        df_bancoBrasil["transaction_type"] = df_bancoBrasil[
            "transaction_type"
        ].str.strip()
        map_rename_transaction = {
            "Tarifa MSG": "Tarifa Bancária",
            "Tarifa MSG - Mês Anterior": "Tarifa Bancária",
            "Pix - Recebido": "Pix Recebido",
            "Seguro de Vida": "Seguro",
            "Cobrança de Juros": "Juros",
            "Cobrança de I.O.F.": "IOF",
            "Compra com Cartão": "Compra Débito",
            "Saque no TAA": "Saque",
            "Recebimento Fornecedor": "Crédito/Rendimento",
            "Pix - Enviado": "Pix Enviado",
            "Pagto cartão crédito": "Pagto Fatura Cartão",
            "Pagamento de Impostos": "Impostos e Tributos",
            "TED Transf.Eletr.Disponiv": "TED Enviado",
            "TEDinternet": "Cobrança TED",
            "Estorno de Débito": "Estorno",
        }
        df_bancoBrasil["transaction_type"] = df_bancoBrasil["transaction_type"].replace(
            map_rename_transaction
        )

        # Criando coluna de categoria do gasto
        map_category = {
            "Tarifa Bancária": "Taxas Bancárias",
            "Pix Recebido": "Pix",
            "Seguro": "Despesas Fixas",
            "Juros": "Taxas Bancárias",
            "IOF": "Taxas Bancárias",
            "Compra Débito": "Despesas Variaveis",
            "Saque": "Dinheiro",
            "Crédito/Rendimento": "Salário",
            "Pix Enviado": "Transferência",
            "Pagto Fatura Cartão": "Cartão de credito",
            "Impostos e Tributos": "Impostos",
            "TED Enviado": "Transferência",
            "Cobrança TED": "Taxas Bancárias",
            "Estorno": "Ajustes",
        }
        df_bancoBrasil["category"] = df_bancoBrasil["transaction_type"].replace(
            map_category
        )

        df_bancoBrasil["bank"] = "Banco do Brasil"

        # print(df_bancoBrasil.to_string())
        # print(df_saldo.to_string())
        # print(df_bancoBrasil.dtypes)

        return df_bancoBrasil
