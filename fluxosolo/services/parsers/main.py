from pathlib import Path

from factory import detect_bank_parser

if __name__ == "__main__":
    CAMINHO_ATUAL = Path(__file__).resolve()
    # Exemplo de caminho
    #arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "NU_414920686_01JAN2026_31JAN2026.csv"
    arquivo_teste = CAMINHO_ATUAL.parent.parent.parent / "data" / "Extrato conta corrente - 012026.csv"
    
    try:
        # 1. A Factory decide QUAL parser usar
        parser = detect_bank_parser(arquivo_teste)
        print(f"Parser escolhido: {parser.__class__.__name__}")
        
        # 2. O Parser faz o trabalho sujo (seguindo o contrato BaseParser)
        df = parser.parser(str(arquivo_teste))
        
    except ValueError as e:
        print(f"Erro: {e}")