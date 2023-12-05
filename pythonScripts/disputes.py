import csv


# Read consults from csv file:
consultas = []
with open('files/Match.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultas.append((row['\ufeffid_match'], row['date'], row['home_team'], row['away_team']))


# Process each consult:
for consulta in consultas:
    match_id, fecha, equipo_local, equipo_visitante = consulta

    datos = [[match_id, equipo_local, True], [match_id, equipo_visitante, False]]

    # Write the data in a CSV file:
    with open('disputes.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write data
        csvwriter.writerows(datos)

    print("Data from consult " + consulta[0] + "has been saved in 'disputes.csv'.")