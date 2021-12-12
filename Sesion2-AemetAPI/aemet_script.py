import requests
import json

from requests.api import request

# In this script some API requests are send to AEMET API. This API contains weather information data from Spain

# loading the api keys dictionary file
with open("./keys.json", "r") as ifile:
    keys = json.load(ifile)
    
'''
request to inventario de estaciones
    searching in the response the field indicativo equals to MADRID, CIUDAD UNIVERSITARIA
    the function returns the value of indicativo
'''
def inventario_estaciones():
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"
    headers = {"api_key":keys["aemet_api_key"]}
    response = requests.get(url, headers)
    json = response.json()
    data_url = json["datos"]
    data_response = requests.get(data_url)
    json_response = data_response.json()
    for estacion in json_response:
        if estacion["nombre"] == "MADRID, CIUDAD UNIVERSITARIA":
            idema = estacion["indicativo"]
    return idema

'''
request to climatologias diarias endpoint
    the field indicativo returned by the function parameter of the function inventario_estaciones is given as a parameter
    returns the url with the climatological values for the selected date range and the selected station
'''
def climatologias_diarias(idema):
    url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/estacion/{idema}"
    url = url.format(fechaIniStr="2019-10-01T00:00:00UTC",
    fechaFinStr="2019-10-30T23:59:59UTC",
    idema="3194U")
    headers = {"api_key":keys["aemet_api_key"]}
    response = requests.get(url, headers=headers)
    url_response = response.json()["datos"]
    return url_response

'''
request to the endpoint that gives the climatological values for all the stations in the selected date range
    downloading all the average temperatures data from all the stations registered in August from 2011 to 2020
    then computing the average anual temperature and returning an array with the average national temperature from each year  
'''
def temperaturas_todas_estaciones():
    temperatura_nacional = []
    for year in range(11, 21):
        url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones"
        year_ini = "20{year}-08-01T00:00:00UTC"
        year_ini = year_ini.format(year=str(year))
        year_fin = "20{year}-08-31T23:59:59UTC"
        year_fin = year_ini.format(year=str(year))
        url = url.format(fechaIniStr=year_ini, fechaFinStr=year_fin)
        headers = {"api_key":keys["aemet_api_key"]}
        response = requests.get(url, headers=headers)
        json = response.json()
        data_url = json["datos"]
        data_response = requests.get(data_url)
        json_response = data_response.json()
        for estacion in json_response:
            if("tmed" in estacion):
                temperaturas_anual = []
                temperatura_media = estacion["tmed"]
                temperaturas_anual.append(temperatura_media)
        media_anual = temp_media_anual(temperaturas_anual)
        temperatura_nacional.append(media_anual)
    return temperatura_nacional

# this function computes the average temperature registered in one year given an array of temperatures
def temp_media_anual(temperaturas):
    suma = 0
    for t in temperaturas:
        suma += float(t.replace(',', '.'))
    media = suma/len(temperaturas)
    return media

if __name__ == "__main__":
    
    idema = inventario_estaciones()
    print("The value of indicativo field for the station Madrid, Zona Universitaria is:")
    print(idema)
    url_clima_ciudad_universitaria = climatologias_diarias(idema)
    print("Click on the url to access the climatological values from MADRID, CIUDAD UNIVERSITARIA in the given date:")
    print(url_clima_ciudad_universitaria)
    
    print("The average temperatures in Spain for the month August from year 2011 to year 2020 are:")
    lista_temperaturas_medias = temperaturas_todas_estaciones()
    print(lista_temperaturas_medias)
