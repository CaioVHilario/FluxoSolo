

from fluxosolo.services.parsers.factory import detect_bank_parser

# CAMINHO_ATUAL = Path(__file__).resolve()
# # Exemplo de caminho
# #arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "NU_414920686_01JAN2026_31JAN2026.csv"
# #arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "Extrato conta corrente - 082023.csv"
# arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "sicoob_2024_02_21_10_58_48.pdf"


def read_extract_file(filepath):

    try:
        # A Factory decide qual parser usar
        parser = detect_bank_parser(filepath)
        print(f"Parser escolhido: {parser.__class__.__name__}")
        
        # O Parser faz o trabalho sujo (seguindo o contrato BaseParser)
        df = parser.parser(filepath)
        print(df)
        
    except ValueError as e:
        print(f"Erro: {e}")
    
    return df