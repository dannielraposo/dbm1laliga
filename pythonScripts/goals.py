from asyncio import sleep
import time
import requests
from bs4 import BeautifulSoup
import csv

# Función para extraer datos y formatearlos
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


# Leer las consultas desde un archivo CSV
consultas = []
with open('consulterror2.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultas.append((row['\ufeffMatch'], row['Fecha'], row['Equipo Local'], row['Equipo Visitante']))


# Procesar cada consulta
for consulta in consultas:
    match_id, fecha, equipo_local, equipo_visitante = consulta

    # Construir la consulta para buscar el partido de fútbol en Google
    query = f"{fecha} {equipo_local} {equipo_visitante}"

    # Realizar la búsqueda en Google y obtener el HTML de la página de resultados
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar el elemento por clase o identificador en el HTML
    clase_o_identificador = "imso_gs__gs-r"
    elementos = soup.findAll(class_=clase_o_identificador)

    datos = []

    # Procesar cada elemento y extraer los datos
    for e in elementos:
        goles = extraer_datos(e, match_id)
        datos.extend(goles)

    # Escribir los datos en un archivo CSV
    with open('goles.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribir datos
        csvwriter.writerows(datos)

    print("Los datos de la consulta " + consulta[0] + "se han guardado en 'goles.csv'.")

    time.sleep(1)