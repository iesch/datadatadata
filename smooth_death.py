import json
from collections import Counter
import string

# --------------
# PREPARING DATA
# --------------

# load the wiki data
data = []
alphabet = 'A' #list(string.ascii_uppercase)
for letter in alphabet :
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

deathplace = {}
deathcount = {}

start, stop, step = 1800, 2030, 10

for time in range(start, stop, step):
    deathplace[time] = []
    deathcount[time] = Counter()

# ------------------
# FILTERING FOR TIME
# ------------------

# filter for only entries that include death place
for person in data:
    for info in person:
        if 'ontology/deathPlace_label' in info and 'ontology/deathDate' in info:
            if not isinstance(info['ontology/deathDate'], list):
                try:
                    year = int(info['ontology/deathDate'].split('-')[0])
                except ValueError:
                    year = 0
                    
                for time in range(start, stop, step):
                    if year >= time and year < time+10:
                        deathplace[time].append(info['ontology/deathPlace_label'])         

# -----------------------------
# FILTERING FOR LOCATION & TIME
# -----------------------------

# counting number of deaths in each place
for time in range(start, stop, step):
    for places in deathplace[time]:
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
                    if place in deathcount[time]:
                        deathcount[time][place] += 1
                    else:
                        deathcount[time][place] = 1
        
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
                if places in deathcount[time]:   
                    deathcount[time][places] += 1          
                else:
                    deathcount[time][places] = 1


# # computing percentages
# perc_deathcount = {'19': Counter(), '21': Counter()}

# for century in deathcount:
#     total = sum((deathcount[century].values()))
#     for country in deathcount[century]:
#         perc_deathcount[century][country] = round((deathcount[century][country] / total) * 100, 2)


# turning final_deathcount into a csv
with open('Results/time_deathcount.csv', 'w', encoding='utf-8') as file:
    file.write('region, year, deathcount\n')
with open(f'Results/time_deathcount.csv', 'a', encoding='utf-8') as file:
    for year in deathcount:
        for key, value in deathcount[year].items():
            file.write(f'{key}, {year}, {value}\n')