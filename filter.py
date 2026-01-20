import json
from collections import Counter
import string
alphabet = list(string.ascii_uppercase)

data = []
# load the data
for letter in alphabet :
    with open(f'People/{letter}_people.json') as file:
        data.append(json.load(file))

# initialize variables
deathplace = []
deathcount = {}
final_deathcount = Counter()

# filter for only entries that include death place
for person in data:
    for info in person: 
        if 'ontology/deathPlace_label' in info and 'ontology/deathDate' in info:
            if not isinstance(info['ontology/deathDate'], list):
                try:
                    year = int(info['ontology/deathDate'].split('-')[0])
                except ValueError:
                    print(info['ontology/deathDate'].split('-')[0])
                if year >= 2000:
                    deathplace.append(info['ontology/deathPlace_label'])

# counting number of deaths in each place
for places in deathplace:
    # if it's a list
    if isinstance(places, list): 
        for place in places:
            place = place.lower()
            if place in deathcount:
                deathcount[place] += 1
                # filter for values above 10
                if deathcount[place] >= 10:
                    final_deathcount[place] = deathcount[place]
            else:
                deathcount[place] = 1
    # if it's a string
    else:                       
        places = places.lower()
        if places in deathcount:   
            deathcount[places] += 1
            # filter for values above 10
            if deathcount[places] >= 10:
                final_deathcount[places] = deathcount[places]
        else:
            deathcount[places] = 1

print(final_deathcount)