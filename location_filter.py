import json
from collections import Counter

# load people data
with open('People/A_people.json') as file:
    data = json.load(file)

# load country with corresponding capital csv
with open('country_capital.csv') as file:
    table = file.read()
# turn csv into a dictionary with country as key and capital as value
country_capital = {}
rows = table.split('\n')
for row in rows:
    country = row.split(';')[0].lower()
    capital = row.split(';')[1].lower()
    country_capital[capital] = country

# load states from US
with open('state_names.txt') as file:
    States = file.read()
# make into a set
States = States.split(',\n')
states = set()
for state in states:
    states.add(state.lower())


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
            
            if place == 'united kingdom':
                place = 'england'

            if place in states:
                place = 'united states'

            # Only count countries 
            if place in country_capital.values():

                # count how many times people died in that country
                if place in country_capital:
                    if place in deathcount:
                        deathcount[place] += 1
                        # filter for values above 10
                        if deathcount[place] >= 10:
                            final_deathcount[place] = deathcount[place]
                    else:
                        deathcount[place] = 1

    # if it's a string i.e. 'Dublin'
    else:                       
        places = places.lower()

        if places == 'united kingdom':
            places = 'england'

        if places in states:
            places = 'united states'
        
        # if it's a capital make it the corresponding country
        if places in country_capital:
            places = country_capital[places] 

        # if it's a country leave it as is
        if places in country_capital.values():
            
            # count how many times people died in that country
            if places in deathcount:   
                deathcount[places] += 1
                # filter for values above 10
                if deathcount[places] >= 10:
                    final_deathcount[places] = deathcount[places]
            else:
                deathcount[places] = 1

print(final_deathcount)