import json
from collections import Counter
import string

# --------------
# PREPARING DATA
# --------------

# load the wiki data
data = []
alphabet = list(string.ascii_uppercase)
for letter in alphabet:
    with open(f'Data/People/{letter}_people.json') as file:
        data.append(json.load(file))

# load country with corresponding capital csv
with open('Data/country_capital.csv') as file:
    table = file.read()
# turn csv into a dictionary with country as key and capital as value
country_capital = {}
rows = table.split('\n')
for row in rows:
    country = row.split(';')[0].lower()
    capital = row.split(';')[1].lower()
    country_capital[capital] = country

# load states from US
with open('Data/state_names.txt') as file:
    States = file.read()
# make into a set
States = States.split(',\n')
states = set()
for state in states:
    states.add(state.lower())

# initialize variables
perc_deathcount = {'19': Counter(), '21': Counter()}
total_wikicount = {'19': 0, '21': 0}
deathplace = {'19': [], '21': []}
deathcount = {'19': Counter(), '21': Counter()}

# ------------------
# FILTERING FOR TIME
# ------------------

# filter for only entries that include death place
for person in data:
    for info in person:
        if 'ontology/deathDate' in info:
            if not isinstance(info['ontology/deathDate'], list):
                try:
                    year = int(info['ontology/deathDate'].split('-')[0])
                except ValueError:
                    year = 0
                if year >= 2000:
                    total_wikicount['21'] += 1
                if year >= 1800 and year < 1900:
                    total_wikicount['19'] += 1
        
        # If the observation has a death date, we do not need to check for a birth date,
        # we do not want to count the same article twice.
        elif 'ontology/birthData' in info:
            if not isinstance(info['ontology/birthDate'], list):
                try:
                    year = int(info['ontology/birthDate'].split('-')[0])
                except ValueError:
                    year = 0
                if year >= 2000:
                    total_wikicount['21'] += 1
                if year >= 1800 and year <1900:
                    total_wikicount['19'] += 1

        if 'ontology/deathPlace_label' in info and 'ontology/deathDate' in info:
            if not isinstance(info['ontology/deathDate'], list):
                try:
                    year = int(info['ontology/deathDate'].split('-')[0])
                except ValueError:
                    year = 0
                if year >= 1800 and year < 1900:
                    deathplace['19'].append(info['ontology/deathPlace_label'])
                if year >= 2000:
                    deathplace['21'].append(info['ontology/deathPlace_label'])

# -----------------------------
# FILTERING FOR LOCATION & TIME
# -----------------------------

# counting number of deaths in each place
for century in deathplace:
    for places in deathplace[century]:
        # if it's a list i.e. ['Paris', 'France']
        if isinstance(places, list): 
            for place in places:
                place = place.lower()
                
                if place == 'england' or place == 'wales' or place == 'scotland':
                    place = 'united kingdom'
                # any state from the US is just counted as US
                if place in states:
                    place = 'united states'

                # Only count countries 
                if place in country_capital.values():
                    
                    # counter 
                    if place in deathcount[century]:
                        deathcount[century][place] += 1
                    else:
                        deathcount[century][place] = 1
        
        # if it's a string i.e. 'Dublin'
        else:                       
            places = places.lower()

            if places == 'england' or places == 'wales' or places == 'scotland':
                places = 'united kingdom'
            # any state from the US is just counted as US
            if places in states:
                places = 'united states'
            
            # if it's a capital make it the corresponding country
            if places in country_capital:
                places = country_capital[places] 

            # if it's a country leave it as is
            if places in country_capital.values():
                
                # counter
                if places in deathcount[century]:   
                    deathcount[century][places] += 1          
                else:
                    deathcount[century][places] = 1

        # -----------------------------
        # SAVING RESULTS IN .CSV FORMAT
        # -----------------------------

    # computing percentages
    total = sum((deathcount[century].values()))
    for country in deathcount[century]:
        perc_deathcount[century][country] = round((deathcount[century][country] / total) * 100, 2)

    # turning final_deathcount and perc_deathcount into a csv 
    with open(f'Results/deathcount_{century}.csv', 'w', encoding='utf-8') as file:
        file.write('Country, Deathcount\n')
        for key, value in deathcount[century].items():
            file.write(f'{key}, {value}\n')
    with open(f'Results/percentage_deathcount_{century}.csv', 'w', encoding='utf-8') as file:
        file.write('Country, Percentage_Deathcount\n')
        for key, value in perc_deathcount[century].items():
            file.write(f'{key.title()}, {value}\n')
