import time
from bs4 import BeautifulSoup
import csv

match = "match380"
html = """  """
# Parsing HTML with BeautifulSoup:
soup = BeautifulSoup(html, 'html.parser')

# Find entries with red and yellow cards:
tarjetas_divs = soup.find_all('div', {'class': 'imso_gf__in-card-hr'})
tarjetas = []

keywords = ['TARJETA AMARILLA', 'TARJETA ROJA']

# Iterate over entries of cards and extract information:
for div in tarjetas_divs:
    texto = div.get_text(strip=True)

    #Verify if the text has the keywords of yellow or red cards:
    if any(keyword in texto for keyword in keywords):
        tipo_tarjeta = 'Yellow' if 'amarilla' in texto.lower() else 'Red'
        nombre_jugador = div.find_next('div', {'class': 'imso_gf__pl-nm'}).text.strip()
        minuto = div.find_next('div', {'class': 'imso_gf__fh-sub'}).text.strip("'")
        if '+' in minuto:
            minuto = int(minuto.split('+')[0].strip()) + int(minuto.split('+')[1].strip())
        tarjetas.append((match, tipo_tarjeta, nombre_jugador, minuto))


# Write data in a csv file:
with open('tarjetas.csv', 'a', encoding='utf-8', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write data:
    csvwriter.writerows(tarjetas)

print("Data of consult has been saved in 'cards.csv'.")