import sys
from bs4 import BeautifulSoup

'''
This script reads an xml file and parses its content using BeautifulSoup
-------------
Params:
    To make this script works, xml file path argument must be given
-------------
Returns:
    Prints xml file content
-------------
Example of execution:
    python xml_reader.py files/"CONVOCATORIAS DE JUNTAS"/BORME-C-2021-8214.xml
'''

if __name__ == "__main__":
    try:
        path = sys.argv[1]
        content = []
        # Read the XML file
        with open(path, encoding='utf-8') as file:
            # Read each line in the file, readlines() returns a list of lines
            content = file.readlines()
            # Combine the lines in the list into a string
            content = "".join(content)
        # Parse file content using BeautifulSoup
        soup = BeautifulSoup(content, "lxml")
        print(soup)
    except:
        print("An error has ocurred, to execute the script you have to write: python xml_reader.py *xml_file_path*")
