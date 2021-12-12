#!/usr/bin/env python3

import logging
from pathlib import Path
import argparse
from camelot import read_pdf
from camelot.core import TableList

logging.basicConfig(
    format="%(levelname)s:%(asctime)s:%(name)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__file__)


def extract_table_from_pdf(pdf_path: str, pages: list, accuracy: int) -> None:
    logger.info(f"Extracting tables from {pdf_path}...")
    tables = read_pdf(filepath=pdf_path, pages=pages, suppress_stdout=False)
    excel_path = Path(Path(pdf_path).parent, f"{Path(pdf_path).stem}.xlsx")
    table_list = []
    for table in tables:
        if table.accuracy >= accuracy:
            table_list.append(table)
    TableList(table_list).export(excel_path, f="excel")
    logger.info(f"Extracted {len(table_list)} tables from {pdf_path}!")


def get_arguments():
    parser = argparse.ArgumentParser(description="Extract tables from PDF file.")
    parser.add_argument(
        "path", type=str, help="Relative path to PDF containing tables to extract."
    )
    parser.add_argument(
        "pages", type=str, help="Example: '1,3,4' or '1,4-end' or 'all'."
    )
    parser.add_argument(
        "--accuracy",
        type=int,
        default=90,
        help="Minimal accuracy for the PDF parser. (Lower value means less restrictive table extraction).",
    )
    args = parser.parse_args()
    return dict(pdf_path=args.path, pages=args.pages, accuracy=args.accuracy)


def main():
    arguments = get_arguments()
    extract_table_from_pdf(**arguments)


if __name__ == "__main__":
    main()
