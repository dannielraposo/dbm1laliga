import time
from bs4 import BeautifulSoup
import csv

match = "match380"
html = """  """
# Parsear el HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Encontrar todas las entradas de tarjetas amarillas y rojas
tarjetas_divs = soup.find_all('div', {'class': 'imso_gf__in-card-hr'})
tarjetas = []

# Palabras clave asociadas a tarjetas amarillas y rojas
keywords = ['TARJETA AMARILLA', 'TARJETA ROJA']

# Iterar sobre las entradas de tarjetas y extraer la información
for div in tarjetas_divs:
    texto = div.get_text(strip=True)

    # Verificar si el texto contiene las palabras clave de tarjetas amarillas o rojas
    if any(keyword in texto for keyword in keywords):
        tipo_tarjeta = 'Yellow' if 'amarilla' in texto.lower() else 'Red'
        nombre_jugador = div.find_next('div', {'class': 'imso_gf__pl-nm'}).text.strip()
        minuto = div.find_next('div', {'class': 'imso_gf__fh-sub'}).text.strip("'")
        if '+' in minuto:
            minuto = int(minuto.split('+')[0].strip()) + int(minuto.split('+')[1].strip())
        tarjetas.append((match, tipo_tarjeta, nombre_jugador, minuto))


# Escribir los datos en un archivo CSV
with open('tarjetas.csv', 'a', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Escribir datos
    csvwriter.writerows(tarjetas)

print("Los datos de la consulta se han guardado en 'tarjetas.csv'.")