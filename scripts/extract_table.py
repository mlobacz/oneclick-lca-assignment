#!/usr/bin/env python3

"""
Extracts tables from given PDF file pages to excel file and places it next to PDF.
"""
import logging
from pathlib import Path
import argparse
from camelot import read_pdf
from camelot.core import TableList

logging.basicConfig(
    format="%(levelname)s:%(asctime)s:%(name)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__file__)


def extract_table_from_pdf(pdf_path: str, pages: str, accuracy: int) -> None:
    """
    Extracts tables from PDF files and saves them in excel file next to PDF.

    Parameters:
        * pdf_path (str): relative path to PDF file
        * pages (str): PDF pages to extract tables from. Example: '1,3,4' or '1,4-end' or 'all'.
        * accuracy (int): Minimal accuracy for the PDF parser.
            (Lower value means less restrictive table extraction).
    """
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
    """
    Returns arguments parsed from the CLI

    Returns:
        * dictionary of arguments names and values from CLI
    """
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
        default=95,
        help="Minimal accuracy for the PDF table parser. (Lower value means less restrictive table extraction).",  # pylint: disable=C0301,
    )
    args = parser.parse_args()
    return dict(pdf_path=args.path, pages=args.pages, accuracy=args.accuracy)


def main():
    """
    Extracts tables from given PDF file to excel file.
    """
    arguments = get_arguments()
    extract_table_from_pdf(**arguments)


if __name__ == "__main__":
    main()
