import requests
from bs4 import BeautifulSoup
import json

# In this script BeautifulSoup is used to extract information about an University from the Wikipedia

# this function create a json file from a dictionary
def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)

if __name__ == "__main__":
    # Loads HTML into soup
    url = "https://en.wikipedia.org/wiki/Comillas_Pontifical_University"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Locates target table with useful info
    target_tables = soup.find_all("table", class_="infobox vcard")
    target_table = target_tables[0]

    # Extract useful information from the table and store in variables
    seal = target_table.find("td", class_="infobox-image").find("img")["src"]
        # aux is used when there is more than one td with the same name
    aux1 = target_table.find_all("td", class_="infobox-full-data")
    motto_latin = aux1[0].find("i").get_text()
    logo = aux1[1].find("img")["src"]
        # aux is used again to store all the td with class name infobox-data
    aux = target_table.find_all("td", class_="infobox-data")
    motto_spanish = aux[0].find("i").get_text()
    motto_english = aux[1].find("i").get_text()
    type = aux[2].get_text()
    established = aux[3].get_text()
    affiliations = aux[4].get_text()
    chancellor = aux[5].get_text()
    vice_chancellor = aux[6].get_text()
    rector = aux[7].get_text()
    students = aux[8].get_text()
    location = aux[9].get_text()
    campus = aux[10].get_text()
    colors = aux[11].get_text()
    website = aux[12].get_text()

    # storing all variables in a dictionary called dic
    dic = {}
    dic['seal'] = seal
    dic['motto_latin'] = motto_latin
    dic['motto_english'] = motto_english
    dic['motto_spanish'] = motto_spanish
    dic['type'] = type
    dic['established'] = established
    dic['chancellor'] = chancellor
    dic['vice_chancellor'] = vice_chancellor
    dic['rector'] = rector
    dic['students'] = students
    dic['location'] = location
    dic['campus'] = campus
    dic['colors'] = colors
    dic['affiliations'] = affiliations
    dic['website'] = website
    dic['logo'] = logo

    # saving the dictionary in a json file
    file_path = "comillas_university.json"
    print_json(dic, file_path)