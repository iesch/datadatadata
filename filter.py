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
total_wikicount = {'19': 0, '21': 0}
deathplace = {'19': [], '21': []}
deathcount = {'19': {}, '21': {}}
final_deathcount = {'19': Counter(), '21': Counter()}

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
        #If the observation has a death date, we do not need to check for a birth date, we do not want to count the same article twice.
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

# counting number of deaths in each place
for century in ['19', '21']:
    for places in deathplace[century]:
        # if it's a list
        if isinstance(places, list): 
            for place in places:
                place = place.lower()
                if place in deathcount[century]:
                    deathcount[century][place] += 1
                    # filter for values above 10
                    if deathcount[century][place] >= 10:
                        final_deathcount[century][place] = deathcount[century][place]
                else:
                    deathcount[century][place] = 1
        # if it's a string
        else:                       
            places = places.lower()
            if places in deathcount[century]:   
                deathcount[century][places] += 1
                # filter for values above 10
                if deathcount[century][places] >= 10:
                    final_deathcount[century][places] = deathcount[century][places]
            else:
                deathcount[century][places] = 1

print(total_wikicount['19'])
print(total_wikicount['21'])
#print(final_deathcount['19'])
#print(final_deathcount['21'])