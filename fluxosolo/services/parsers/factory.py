from Nubank import NubankParser
from BancoBrasil import BancoBrasiParser


def detect_bank_parser(filepath: str):

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                header_line = f.readline().strip()
            detected_encoding = encoding
            break
        except UnicodeDecodeError:
            continue
    
    if header_line is None:
        raise ValueError(F'Don\'t possible read file {filepath}')
    
    header_clean = header_line.replace('"', '')

    if 'Data,Valor,Identificador,Descrição' in header_clean:
        return NubankParser(encoding=detected_encoding)

    if 'Data' in header_clean and 'Lançamento' in header_clean and 'Detalhes' in header_clean:
        return BancoBrasiParser(encoding=detected_encoding)
