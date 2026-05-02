import pandas as pd

from fluxosolo.services.parsers.Base import BaseParser


class NubankParser(BaseParser):
    def __init__(self, encoding):
        self.encoding = encoding

    def _extract_data(self, filepath: str) -> pd.DataFrame:
        # Lê arquivo csv
        df_nubank = pd.read_csv(
            filepath,
            parse_dates=["Data"],
            date_format="%d/%m/%Y",
            encoding=self.encoding,
        )

        # austa colunas e renomeias
        df_nubank[["Transação", "Detalhes"]] = (
            df_nubank["Descrição"].str.split("-", expand=True, n=2).iloc[:, :2]
        )
        df_nubank = df_nubank.drop(["Identificador", "Descrição"], axis=1)

        # Renomeia colunas para inserir dataframen no banco de dados
        map_rename = {
            "Data": "date",
            "Transação": "transaction_type",
            "Detalhes": "details",
            "Valor": "value",
        }
        df_nubank = df_nubank.rename(columns=map_rename)

        # Renomeia transações para padronizar com os outros bancos
        df_nubank["transaction_type"] = df_nubank[
            "transaction_type"
        ].str.strip()
        map_rename_transaction = {
            "Compra no débito": "Compra Débito",
            "Transferência recebida pelo Pix": "Pix Recebido",
            "Pagamento de fatura": "Pagamento Fatura Cartão",
            "Transferência enviada pelo Pix": "Pix Enviado",
        }
        df_nubank["transaction_type"] = df_nubank["transaction_type"].replace(
            map_rename_transaction
        )

        # Cria a coluna category no dataframe
        map_category = {
            "Compra Débito": "Despesas Variaveis",
            "Pix Recebido": "Pix",
            "Pagamento Fatura Cartão": "Cartão de credito",
            "Pix Enviado": "Transferência",
        }
        df_nubank["category"] = df_nubank["transaction_type"].replace(
            map_category
        )

        # Adiciona coluna referente ao banco
        df_nubank["bank"] = "NuBank"

        # print(df_nubank.to_string())
        # print(df_nubank.dtypes)

        return df_nubank
