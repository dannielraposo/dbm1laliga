import csv


# Leer las consultas desde un archivo CSV
consultas = []
with open('files/Match.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultas.append((row['\ufeffid_match'], row['date'], row['home_team'], row['away_team']))


# Procesar cada consulta
for consulta in consultas:
    match_id, fecha, equipo_local, equipo_visitante = consulta

    datos = [[match_id, equipo_local, True], [match_id, equipo_visitante, False]]

    # Escribir los datos en un archivo CSV
    with open('disputes.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribir datos
        csvwriter.writerows(datos)

    print("Los datos de la consulta " + consulta[0] + "se han guardado en 'goles.csv'.")