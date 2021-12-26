## Session 13 - BORME

In this session requests, bs4, selenium and chromedriver is used to download data from newly incorporated companies from the Spanish Mercantile Registry.

borme directory contains the following files:
- __main__.py: This script navigates through https://www.boe.es/diario_borme/ website and find specific sections that correspond to a specific date to download pdf and xml files sorted in directories. To execute it you must provide the date: python __main__.py YYYYMMDD.
- xml_reader.py: This script reads an xml file and parses its content using BeautifulSoup. To execute it you must provide the xml file path: python xml_reader.py xmlfilepath
- /files: directory that contains directories with the pdf and xml files downloaded. After every execution this directory is cleared (deleting all the content inside) and updated with directories (one per subsection) and new files.
