#!/usr/bin/env python

from setuptools import setup

setup(
    name="oneclick-lca-scraper",
    version="1.0",
    description="GreenBookLive PDF files scraper and tables extractor created as a recruitment assignment task.",
    author="Marcin Lobaczewski",
    author_email="m.lobaczewski.dev@gmail.com",
    install_requires=[
        "beautifulsoup4 >= 4.10.0",
        "requests >= 2.26.0",
        "camelot-py[cv] >= 0.10.1",
        "opencv-contrib-python-headless >= 4.5.4.60",
    ],
    scripts=["scripts/scrape_greenbooklive.py", "scripts/extract_table.py"],
)
