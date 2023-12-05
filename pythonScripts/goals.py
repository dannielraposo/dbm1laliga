from asyncio import sleep
import time
import requests
from bs4 import BeautifulSoup
import csv

# Function to extract and format data:
def extraer_datos(elemento, match_id):
    nombre = elemento.find('span').text
    minutos_goles = elemento.find_all('span', class_='imso_gs__g-a-t')
    goles = []
    for minuto_gol in minutos_goles:
        minuto_texto = minuto_gol.text
        minuto_numero = int(''.join(filter(str.isdigit, minuto_texto.split('+')[0])))
        if '+' in minuto_texto:
            tiempo_adicional = int(minuto_texto.split('+')[1].strip("'")[0])
            minuto_numero += tiempo_adicional
        tiene_p = '(P)' in minuto_texto
        tiene_pp = '(PP)' in minuto_texto or '(contre son camp)' in minuto_texto
        goles.append([match_id, nombre, minuto_numero, tiene_p, tiene_pp])
    return goles


# Read consults from csv file:
consultas = []
with open('files/consults.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultas.append((row['\ufeffMatch'], row['Fecha'], row['Equipo Local'], row['Equipo Visitante']))


# Process each consult:
for consulta in consultas:
    match_id, fecha, equipo_local, equipo_visitante = consulta

    # Construct the consult to search the match on Google:
    query = f"{fecha} {equipo_local} {equipo_visitante}"

    # Make the consult on Google and getting HTML of results page
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parsing HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find element in the HTML:
    clase_o_identificador = "imso_gs__gs-r"
    elementos = soup.findAll(class_=clase_o_identificador)

    datos = []

    # Process each element and extract data:
    for e in elementos:
        goles = extraer_datos(e, match_id)
        datos.extend(goles)

    # Write the data in a CSV file:
    with open('goles.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write data:
        csvwriter.writerows(datos)

    print("Data from consult " + consulta[0] + "has been saved in 'goles.csv'.")

    time.sleep(1) #to not get blocked from Google!