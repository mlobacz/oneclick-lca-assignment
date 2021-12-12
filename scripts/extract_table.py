#!/usr/bin/env python3

import logging
from pathlib import Path

from camelot import read_pdf

logging.basicConfig(
    format="%(levelname)s:%(asctime)s:%(name)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__file__)


def extract_table_from_pdf(pdf_path: str, pages: list) -> None:
    logger.info(f"Extracting tables from {pdf_path}...")
    tables = read_pdf(filepath=pdf_path, pages=pages, suppress_stdout=True)
    excel_path = Path(Path(pdf_path).parent, f"{Path(pdf_path).stem}.xlsx")
    for table in tables:
        if table.accuracy == 100:
            table.to_excel(excel_path)
    logger.info(f"Extracted tables from {pdf_path}!")
