#!/usr/bin/env python3

"""
Download all pdf files from GreenBookLive searches into a folder.
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, List
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

URL = "https://www.greenbooklive.com/search/companysearch.jsp?from=0&partid=10028&sectionid=0&companyName=&productName=&productType=&certNo=&regionId=0&countryId=0&addressPostcode=&certBody=&id=260&results_pp=1000&sortResultsComp"  # pylint: disable=C0301


logging.basicConfig(
    format="%(levelname)s:%(asctime)s:%(name)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__file__)


def get_pdf_urls(page_url: str) -> list:
    """
    Get all urls leading to pdf files from GreenBookLive search results page.

    Parameters:
        * page_url (str): url to webpage with GreenBookLive search results.

    Returns:
        * List strings with pdf urls.
    """
    logging.debug("Getting GreenBookLive page content...")
    page_content = requests.get(page_url).content
    soup = BeautifulSoup(page_content, "html.parser")
    logging.debug("Parsing GreenBookLive page for pdf files locations...")
    raw_relative_urls = soup.find(id="search-results").find_all("a")
    relative_urls = [
        raw_relative_url["href"].lstrip("..")
        for raw_relative_url in raw_relative_urls
        if raw_relative_url["href"].endswith(".pdf")
    ]
    return [urljoin(page_url, relative_url) for relative_url in relative_urls]


def file_path_from_url(url: str) -> Path:
    """
    Extract relative file path from URL.

    Parameters:
        * url (str): URL to single PDF file.

    Returns:
        * relative file path (Path)
    """
    return Path(urlsplit(url).path.lstrip("/"))


def prepare_directories(file_paths: List[Path]) -> None:
    """
    Prepares directory structure based on passed file paths

    Parameters:
        * file_paths (list[Path]): list of file paths objects
    """
    for file_path in file_paths:
        directory_structure = file_path.parent
        logging.debug(f"Preparing {directory_structure} directory...")
        directory_structure.mkdir(parents=True, exist_ok=True)


def download_pdf(url: str) -> None:
    """
    Download pdf file from URL.

    Parameters:
        * url (str): URL to single PDF file.
    """
    logger.info(f"Downloading pdf data from: {url}...")
    response = requests.get(url, stream=True)
    file_path = file_path_from_url(url)
    with open(file_path, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=8192):
            pdf_file.write(chunk)
        logger.info(f"Downloaded pdf data from:{url} to: {file_path}!")


def map_function_to_threads(func, args: Iterable) -> None:
    """
    Maps function execution to threads.

    Parameters:
        * func (function): function to be executed in threads
        * args (Iterable): iterable (e.g. list) of arguments to pass to function
    """
    with ThreadPoolExecutor() as executor:
        executor.map(func, args)


def main():
    """
    Scrapes GreenBookLive search results page and downloads found PDF files
    preserving directory structure present on the web page.
    """
    logging.info("Scraping GreenBookLive for pdf files started...")
    pdf_urls = get_pdf_urls(page_url=URL)
    file_paths = [file_path_from_url(url) for url in pdf_urls]
    prepare_directories(file_paths)
    map_function_to_threads(download_pdf, pdf_urls)
    logging.info("Scraping GreenBookLive for pdf files finished!")


if __name__ == "__main__":
    main()
