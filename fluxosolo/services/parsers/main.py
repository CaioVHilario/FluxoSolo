import pandas as pd
from pathlib import Path

from fluxosolo.services.parsers.factory import detect_bank_parser
from fluxosolo.core.database import engine

if __name__ == "__main__":
    CAMINHO_ATUAL = Path(__file__).resolve()
    # Exemplo de caminho
    #arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "NU_414920686_01JAN2026_31JAN2026.csv"
    #arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "Extrato conta corrente - 082023.csv"
    arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "sicoob_2024_02_21_10_58_48.pdf"
    
    try:
        # 1. A Factory decide QUAL parser usar
        parser = detect_bank_parser(arquivo_teste)
        print(f"Parser escolhido: {parser.__class__.__name__}")
        
        # 2. O Parser faz o trabalho sujo (seguindo o contrato BaseParser)
        df = parser.parser(str(arquivo_teste))
        print(df)

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        print('Colocando dados no banco de dados...')

        df.to_sql(
            'transactions',
            con=engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=500,
        )

        print('Ação concluida!')
        
    except ValueError as e:
        print(f"Erro: {e}")