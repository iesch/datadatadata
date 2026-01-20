import json
from collections import Counter

# load people data
with open('People/A_people.json') as file:
    data = json.load(file)

# load list of countries
with open('countries.txt', encoding='utf-8') as file:
   Countries = file.read()

# make a set with all the countires
Countries = Countries.split(',\n')
countries = set()
for Country in Countries:
    countries.add(Country.lower())

# initialize variables
deathplace = []
deathcount = {}
final_deathcount = Counter()

# filter for only entries that include death place
for dict in data: 
    if 'ontology/deathPlace_label' in dict:
        deathplace.append(dict['ontology/deathPlace_label'])

# counting number of deaths in each place
for places in deathplace:
    # if it's a list i.e. ['Paris', 'France']
    if isinstance(places, list): 
        for place in places:
            place = place.lower()
            # check if it's a country
            if place in countries:
                if place in deathcount:
                    deathcount[place] += 1
                    # filter for values above 10
                    if deathcount[place] >= 10:
                        final_deathcount[place] = deathcount[place]
                else:
                    deathcount[place] = 1
    
    # if it's a string i.e. 'Ireland'
    else:                       
        places = places.lower()
        # check if it's a country
        if places in countries:
            if places in deathcount:   
                deathcount[places] += 1
                # filter for values above 10
                if deathcount[places] >= 10:
                    final_deathcount[places] = deathcount[places]
            else:
                deathcount[places] = 1

print(final_deathcount)