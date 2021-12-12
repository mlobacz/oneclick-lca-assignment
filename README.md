# OneClick LCA Test Assignment

## Task 1 description

Scrape a [web page](https://www.greenbooklive.com/search/companysearch.jsp?from=0&partid=10028&sectionid=0&companyName=&productName=&productType=&certNo=&regionId=0&countryId=0&addressPostcode=&certBody=&id=260&results_pp=1000&sortResultsComp) 
and download all pdf files from the page into a folder.


## Task 2 description

After the download process is done, choose 2 pdf files and extract any table from files into an excel file.

## Solution description

For each task, separate python script was created. Each of them is configurable through provided CLI interface.

## How to install and run scripts.

1. Clone this git repository

    ```bash
    git clone git@github.com:mlobacz/oneclick-lca-assignment.git
    ```

2. Change into projects root directory.

    ```bash
    cd oneclick-lca-assignment
    ```

3. Create and activate new virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Install python package with the scripts

    ```bash
    pip install --upgrade pip
    pip install . --no-cache-dir (last flag is optional, but may be needed in case of issues with dependecies)
    ```

5. (OPTIONAL) At this moment, both scraping and extracting pfds should work fine. Extracting tables however, may need some extra dependecies. If necessary check the details in [camelot documentation](https://camelot-py.readthedocs.io/en/master/user/install-deps.html).

   * For Ubuntu
    ```bash
    apt install ghostscript python3-tk
    ```
   * For MacOS
    ```bash
    brew install ghostscript tcl-tk
    ```

6. To scrape PDF files from GreenBookLive search results run:

    ```bash
    python3 scripts/scrape_greenbooklive.py
    ```
    Scraping will be executed in threads with default URL (given in the task definition) and results will be saved in the location where script was run from, preserving directory structure present on the web page.
    
    However, custom URL may be also provided with the use of `--url` argument (some chars like = or ? need to be escaped), for example for page with different search parameters.
    ```bash
    python3 scripts/scrape_greenbooklive.py --url https://www.greenbooklive.com/search/companysearch.jsp\?partid\=10028\&sectionid\=0\&companyName\=\&productName\=\&productType\=\&certNo\=\&regionId\=0\&countryId\=0\&addressPostcode\=\&certBody\=\&id\=260\&sortResultsComp\=
    ```

7. To extract tables from some PDF file run:
    ```bash
    python3 scripts/extract_table.py [relative_path_to_pdf] [comma delimited numbers of pages with tables] [accuracy(optional)]
    ```
    for example below commands will extract tables from all pages of `pdfdocs/mrepd/R00024.pdf` and `pdfdocs/mrepd/R00025.pdf` files with default accuracy of 95.
    ```bash
    python3 scripts/extract_table.py pdfdocs/mrepd/R00024.pdf all
    python3 scripts/extract_table.py pdfdocs/mrepd/R00025.pdf all
    ```
    for help (like example page values) type:
    ```bash
    python3 scripts/extract_table.py -h
    ```
    


## (optional) How to configure development environment.
1. Create and activate new virtual environment (if not created already)

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2. Install pip-tools

    ```bash
    pip install --upgrade pip
    pip install pip-tools
    ```

3. Install python requirements

    ```bash
    pip-sync requirements.txt dev-requirements.txt
    ```

4. You may want to check the code quality:


    ```bash
    mypy scripts
    pylint scripts
    ```
