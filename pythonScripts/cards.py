import time
import requests
from bs4 import BeautifulSoup
import csv
from googlesearch import search


# Leer las consultas desde un archivo CSV
consultas = []
with open('consultstry.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultas.append((row['\ufeffMatch'], row['Fecha'], row['Equipo Local'], row['Equipo Visitante']))


# Procesar cada consulta
for consulta in consultas:
    match_id, fecha, equipo_local, equipo_visitante = consulta

    # Construir la consulta para buscar el partido de fútbol en Google
    query = f"{fecha} {equipo_local} {equipo_visitante} transfermarkt cards amonestaciones informe"

    # Realizar la búsqueda en Google
    resultados = search(query, num=1, stop=1, pause=2)

    # Obtener la URL del primer resultado de la búsqueda
    url = next(resultados)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Encontrar todos los elementos h2 con clase "content-box-headline"
    h2_elements = soup.find_all("h2", class_="content-box-headline")

    # Iterar sobre los elementos h2 y encontrar el div con clase "sb-ereignisse" que sigue al h2 con texto "Cards"
    target_div = None
    for h2 in h2_elements:
        if h2.get_text(strip=True) == "Cards" or h2.get_text(strip=True) == "Amonestaciones":
            target_div = h2.find_next(class_="sb-ereignisse")
            break

    # Parsear el fragmento de HTML con BeautifulSoup
    soup = BeautifulSoup(str(target_div), 'html.parser')

    # Encontrar todos los elementos <li> dentro del <ul>
    try:
        tarjetas = soup.find('div', class_='sb-ereignisse').ul.find_all('li')
    except:
        # Escribir los datos en un archivo CSV
        with open('tarjetas.csv', 'a', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Escribir datos
            csvwriter.writerows([[match_id, 'null', 'null','null']])
        continue


    # Lista para almacenar la información de las tarjetas amarillas
    tarjetas_info = []

    # Extraer tipo de tarjeta, nombre del jugador y motivo de tarjeta para cada tarjeta amarilla
    for tarjeta in tarjetas:
        nombre_jugador = tarjeta.find('div', class_='sb-aktion-aktion').a.get_text(strip=True)
        tipo_tarjeta = tarjeta.find('div', class_='sb-aktion-aktion').contents[-1].strip().split(",")[0].split('.')
        if len(tipo_tarjeta) == 1:
            tipo_tarjeta = tipo_tarjeta[0].strip()
        else:
            tipo_tarjeta = tipo_tarjeta[1].strip()
        motivo = tarjeta.find('div', class_='sb-aktion-aktion').contents[-1].strip().split(",")
        if len(motivo)<2:
            motivo_tarjeta = 'unknown'
        else:
            motivo_tarjeta = motivo[1].strip()
        tarjetas_info.append([match_id, nombre_jugador, tipo_tarjeta, motivo_tarjeta])

    # Escribir los datos en un archivo CSV
    with open('tarjetas.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribir datos
        csvwriter.writerows(tarjetas_info)

    print("Los datos de la consulta " + consulta[0] + " se han guardado en 'tarjetas.csv'.")

    time.sleep(1)