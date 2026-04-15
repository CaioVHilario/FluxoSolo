from fluxosolo.services.parsers.factory import detect_bank_parser


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
