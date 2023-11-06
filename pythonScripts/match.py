import csv

# Leer las consultas desde un archivo CSV
matches = []
with open('files/Match.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        matches.append((row['\ufeffid_match'], row['date'], row['home_team'], row['away_team'], row['winner_team_FT'], row['winner_team_HT']))


teams = []
with open('files/Team.csv',encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        teams.append((row['\ufeffteam_name'], row['city'], row['year'], row['stadium'], row['president']))

# Procesar cada consulta
for match in matches:
    match_id, date, home_team, away_team, winner_team_FT,winner_team_HT = match
    
    stadium = None
    for team in teams:
        if team[0] == home_team:
            stadium = team[3]


    # Escribir los datos en un archivo CSV
    with open('matchNew.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Escribir datos
        csvwriter.writerow([match_id, date, stadium, winner_team_FT, winner_team_HT ])

    print("Los datos de la consulta " + match[0] + "se han guardado en 'matchNew.csv'.")