from pathlib import Path

import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError

from fluxosolo.services.parsers.BancoBrasil import BancoBrasiParser
from fluxosolo.services.parsers.Nubank import NubankParser
from fluxosolo.services.parsers.Sicoob import SicoobParser


def detect_bank_parser(filepath: str | Path):

    # verifica se é pdf e em seguida verifica se é um extrato do sicoob para 
    # usar seu parser
    if filepath.name.lower().endswith(".pdf"):
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
        except (
            PDFSyntaxError,
            FileNotFoundError,
            TypeError,
            AttributeError,
        ) as e:
            raise ValueError(f"Error reading PDF for detection {e}")

    # verifica se é um .csv e se for vê se é um extrato do BB ou NuBank para 
    # usar op respectivo parser
    elif filepath.name.lower().endswith(".csv"):
        encodings_to_try = ["utf-8", "latin-1", "cp1252"]

        for encoding in encodings_to_try:
            try:
                filepath.seek(0)

                line_bytes = filepath.readline()
                header_line = line_bytes.decode(encoding)
                filepath.seek(0)
                detected_encoding = encoding
                break
            except UnicodeDecodeError:
                continue

        if header_line is None:
            raise ValueError(f"Don't possible read file {filepath}")

        header_clean = header_line.replace('"', "")

        if "Data,Valor,Identificador,Descrição" in header_clean:
            return NubankParser(encoding=detected_encoding)

        if (
            "Data" in header_clean
            and "Lançamento" in header_clean
            and "Detalhes" in header_clean
        ):
            return BancoBrasiParser(encoding=detected_encoding)
