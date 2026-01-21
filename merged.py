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
    if len(row.split(';')) == 2:
        country = row.split(';')[0]
        capital = row.split(';')[1]
        country_capital[capital] = country

# load states from US
with open('Data/state_names.txt') as file:
    states = file.read()
# make into a set
states = states.split(',\n')
states = set()
for State in states:
    states.add(State.title())

# initialize variables
centuries = ['19', '20', '21']
perc_deathcount = {}
deathplace = {}
deathcount = {}

for century in centuries:
    perc_deathcount[century] = Counter()
    deathplace[century] = []
    deathcount[century] = Counter()

# ------------------
# FILTERING FOR TIME
# ------------------

# filter for only entries that include death place & death date
for person in data:
    for info in person:
        if 'ontology/deathPlace_label' in info and 'ontology/deathDate' in info:
            if not isinstance(info['ontology/deathDate'], list):
                try:
                    year = int(info['ontology/deathDate'].split('-')[0])
                except ValueError:
                    year = 0
                if year >= 1800 and year < 1900:
                    deathplace['19'].append(info['ontology/deathPlace_label'])
                if year >= 1900 and year < 2000:
                    deathplace['20'].append(info['ontology/deathPlace_label'])
                if year >= 2000:
                    deathplace['21'].append(info['ontology/deathPlace_label'])

# -----------------------------
# FILTERING FOR LOCATION
# -----------------------------

# counting number of deaths in each place
for century in centuries:
    for places in deathplace[century]:
        # if it's a list i.e. ['Paris', 'France']
        if isinstance(places, list): 
            for place in places:
                
                if place == 'England' or place == 'Wales' or place == 'Scotland':
                    place = 'UK'
                # any state from the US is just counted as US
                if place in states or place == 'United States of America' or place == 'United States':
                    place = 'USA'

                # Only count countries 
                if place in country_capital.values():
                    
                    # counter 
                    if place in deathcount[century]:
                        deathcount[century][place] += 1
                    else:
                        deathcount[century][place] = 1
        
        # if it's a string i.e. 'Dublin'
        else:                       
            if places == 'England' or places == 'Wales' or places == 'Scotland':
                places = 'UK'
            # any state from the US is just counted as US
            if places in states or places == 'United States of America' or places == 'United States':
                places = 'USA'
            
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

with open('Results/deathcount.csv', 'w', encoding='utf-8') as file:
    file.write('region, century, deathcount\n')
with open('Results/deathcount.csv', 'a', encoding='utf-8') as file:
    for century in centuries:
        # turning final_deathcount and perc_deathcount into a csv 
        for key, value in deathcount[century].items():
            file.write(f'{key}, {century}, {value},\n')


with open('Results/percentage_deathcount.csv', 'w', encoding='utf-8') as file:
    file.write('region, century, Percentage_Deathcount\n')
for century in centuries:
    # computing percentages
    total = sum((deathcount[century].values()))
    for country in deathcount[century]:
        perc_deathcount[century][country] = round((deathcount[century][country] / total) * 100, 2)

    with open('Results/percentage_deathcount.csv', 'a', encoding='utf-8') as file:
        for key, value in perc_deathcount[century].items():
            file.write(f'{key}, {century}, {value}\n')