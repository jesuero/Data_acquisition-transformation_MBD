import requests
from bs4 import BeautifulSoup
import json

'''
In this script BeautifulSoup is used to extract information from a Wikipedia's website that contains 
 a table with the world population per continent, and store it in a JSON file.
'''

# this function create a json file from a dictionary
def print_json(dic, file_path):
    with open(file_path, "w") as output_file:
        json.dump(dic, output_file)

if __name__ == "__main__":
    # Loads HTML into soup
    url = "https://en.wikipedia.org/wiki/World_population"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Locates target table with useful info
    target_tables = soup.find_all("table", class_="wikitable sortable")
    target_table = target_tables[0]

    # Creates a list of dictionaries (one dictionary for each row of the table) and loop over the rows.
    dic = []
    for i in range(1,len(target_table.find_all("tr"))-1):
        dic_country = {}
        aux = target_table.find_all("tr")[i].find_all("td")
        dic_country['continent'] = aux[0].get_text()[:-1]
        dic_country['density'] = aux[1].get_text()[:-1]
        dic_country['population'] = aux[2].get_text()[:-1]
        dic_country['populous-country'] = aux[3].get_text()[:-1].replace("\u2013","").replace("\u00a0","")
        dic_country['populous-city'] = aux[4].get_text()[:-1].replace("\u2013","")
        dic.append(dic_country)
        
    # saving the dictionary in a json file
    file_path = "world-population.json"
    print_json(dic, file_path)
