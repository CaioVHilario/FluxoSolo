from pathlib import Path
import pdfplumber

from fluxosolo.services.parsers.Nubank import NubankParser
from fluxosolo.services.parsers.BancoBrasil import BancoBrasiParser
from fluxosolo.services.parsers.Sicoob import SicoobParser

def detect_bank_parser(filepath: str | Path):

    if filepath.suffix.lower() == '.pdf':
        page_num = 0
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_num += 1
                    first_page_text = page.extract_text()
                    if page_num > 0:
                        break
            if "SICOOB" in first_page_text and "EXTRATO" in first_page_text:
                return SicoobParser()
        except Exception as e:
            raise ValueError(f"Error reading PDF for detection {e}")


    elif filepath.suffix.lower() == '.csv':
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
