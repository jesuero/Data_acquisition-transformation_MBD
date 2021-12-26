import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from os import makedirs
from os.path import exists
import shutil

'''
This script navigates through https://www.boe.es/diario_borme/ website and find specific sections 
that correspond to a specific date to download pdf and xml files sorted in directories. 
This is done using requests, Selenium, Chromedriver and BeautifulSoup.
'''

def load_boe(date): 
        '''
        This function takes a date and checks if there is a borme published
        -------------
        Params:
        Date: string with date format YYYYMMDD
        -------------
        Returns:
        url: string with url format. Is the url from the borme published on that date
        If no borme published on that date the function does not return anything.
        '''
        # parsing the date
        year = date[0:4]
        month = date[4:6]
        day = date[6:9]
        # constructing the url with date parameters
        url = "https://www.boe.es/borme/dias/{y}/{m}/{d}/".format(y=year,m=month,d=day)
        
        # if there is a borme published on the date, response code must be 200
        response_code = requests.get(url).status_code
        if(response_code==200):
                return url

def get_pdf_urls(url):
        '''
        This function takes a url from a borme published on a specific day and navigate the website
        using Selenium to find subsections names and collect pdf files urls.
        -------------
        Params:
        url: string url (from boe website) of a borme for a concrete day.
        -------------
        Returns:
        list_directories: list of lists. Size equal the number of subsections from the borme of that day.
                        Each list inside list_directories contains the name of the subsection (string) 
                        and a list (string list) with all the pdf files urls for each subsection.
                        Example: [["Subsection name", [https://www.boe.es/filename.pdf, file.pdf, ...]],
                                        [Subsection2 name, [https://file2.pdf, ...]],...]
        '''
        # initialize webdriver chromedriver headless (no interface)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
                executable_path="../../chromedriver.exe",
                chrome_options=chrome_options
                )
        # get url from params
        driver.get(url)
        # introduce time sleep between actions (don't want to make a lot of petitions in short time period)
        time.sleep(2)
        # find and click desplegable menu
        input_seccciones = driver.find_element_by_class_name("desplegable")
        input_seccciones.click()
        time.sleep(2)
        # find the div containing the section wanted (Sección Segunda. Anuncios y avisos legales)
        div_dropdown = driver.find_element_by_class_name("dropdown")
        # find the li that have the link to the section and click it
        seccion_segunda = div_dropdown.find_elements_by_tag_name("li")[4]
        seccion_segunda.find_element_by_tag_name("a").click()
        time.sleep(2)
        
        # store in list_directories all the subsections names in a list (found in h4 tags)
        list_directories = []
        div_summary = driver.find_element_by_class_name("sumario")
        directory_names = div_summary.find_elements_by_tag_name("h4")
        for name in directory_names:
                list_directories.extend([[name.text]])
        
        # find all the ul tags inside the correspond div (subsections) and iterate over them extracting the pdf files links 
        list_ul_urls = driver.find_elements_by_xpath("//div[@class='sumario']/ul")
        for i in range(len(list_ul_urls)):
                li_files = list_ul_urls[i].find_elements_by_class_name("puntoPDF")
                # store the links in a list and add them to the subsection list (next to the name previously extracted)
                list_urls_subseccion = [li.find_element_by_tag_name("a").get_attribute("href") for li in li_files]
                list_directories[i].extend([list_urls_subseccion])
        # close the driver so it do not continue running in background
        driver.close()
        return list_directories

def get_xml_urls(url):
        '''
        This function takes a url from a borme published on a specific day and navigate the website
        using BeautifulSoup to find the xml version of the website. Then parses the xml website again with
        BeautifulSoup and iterate over the subsections collecting xml files urls.
        -------------
        Params:
        url: string url (from boe website) of a borme for a concrete day.
        -------------
        Returns:
        list_urls: list of lists. Size equal the number of subsections from the borme of that day.
                Each list inside list_urls contains a list (string list) with all the xml files urls for each subsection.
        '''
        # BeautifulSoup to find the borme url in xml format
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        url_xml = soup.find("li", class_="puntoXML").find("a")["href"]
        url_xml = "https://www.boe.es/" + url_xml
        
        # Parse xml with BeautifulSoup to find all the xml files urls by subsection
        xml_response = requests.get(url_xml)
        xml_soup = BeautifulSoup(xml_response.content, "xml")
        subsections = xml_soup.find("seccion", num="C").find_all("emisor")
        list_urls = []
        # iterate over the subsections list
        for sec in subsections:
                urls = sec.find_all("urlXml")
                ls_aux = []
                # iterate over the xml files urls on every subsection
                for url in urls:
                        xml = "https://www.boe.es" + url.get_text()
                        ls_aux.append(xml)
                list_urls.extend([ls_aux])
        return list_urls

def download_files(list_urls):
        '''
        This function takes the list that contains subsections names, pdf files urls and xml files urls, 
        and create directories in project directory /files to download the files inside.
        -------------
        Params:
        list_urls: list of lists. Each list contains: 
                - directory name, subsection name (string)
                - pdf files urls (string list)
                - xml files urls (string list)
        -------------
        Returns:
        prints a message.
        '''
        # first, clear the files directory to delete files from previous executions
        files_dir = "files"
        if exists(files_dir):
                shutil.rmtree(files_dir)
        makedirs(files_dir)
        # loops over every subsection creating a directory with its name and downloading files on each one
        for subsection in list_urls:
                directory = subsection[0]           
                makedirs(files_dir + "/" + directory)
                # loop over the pdf lists for every subsection and download using requests
                for pdf in subsection[1]:
                        filename = pdf.split('/')[-1]
                        response = requests.get(pdf)
                        with open(files_dir + "/" + directory + "/" + filename, 'wb') as output_file:
                                output_file.write(response.content)
                # loop over the xml lists for every subsection and download using requests
                for xml in subsection[2]:
                        filename = xml.split('=')[-1] + ".xml"
                        response = requests.get(xml)
                        with open(files_dir + "/" + directory + "/" + filename, 'wb') as output_file:
                                output_file.write(response.content)
        return print("##### All files successfully downloaded")

if __name__ == "__main__":
        # Checks if arguments where given and if they are in the correct format
        try:
                arguments = sys.argv[1]
                if(len(arguments) != 8):
                        print("Please introduce the date in the correct format: YYYYMMDD (year, month, day)")
                else:
                        # if arguments given propertly check if borme exists for that date
                        boe = load_boe(arguments)
                # if exists...
                if(boe):
                        # save in list_urls directory names of sections and lists of pdf file urls
                        list_urls = get_pdf_urls(boe)
                        print("All pdf urls has been collected properly")
                        # save in ls_xml lists of xml files urls
                        ls_xml = get_xml_urls(boe)
                        print("All xml urls has been collected properly")
                        # add xml files collected to list_urls
                        for i in range(len(list_urls)):
                                list_urls[i].append(ls_xml[i])
                        # call function to create directories and download all pdf and xml files
                        download_files(list_urls)

                # if boe doesn't exist print error
                else:
                        print("An error has ocurred, maybe in the date introduced no BOE was published, try with another date or try again the same execution")
        except:
                print("No arguments given, to execute the script you have to write: python __main.py__ YYYYMMDD")
