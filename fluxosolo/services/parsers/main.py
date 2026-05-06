from fluxosolo.services.parsers.factory import detect_bank_parser


def read_extract_file(file_name, bytes_content: bytes):

    try:
        # A Factory decide qual parser usar
        parser = detect_bank_parser(file_name, bytes_content)
        print(f"Parser escolhido: {parser.__class__.__name__}")

        # O Parser faz o trabalho sujo (seguindo o contrato BaseParser)
        df = parser.parser(bytes_content)
        print(df)

    except ValueError as e:
        print(f"Erro: {e}")

    return df
