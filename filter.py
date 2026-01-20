import json

# load the data
with open('People/A_people.json') as file:
    data = json.load(file)

deathplace = []
for row in data: 
    if 'ontology/deathPlace_label' in row:
        deathplace.append(row['ontology/deathPlace_label'])

deathcount = {}
final_deathcount = {}

for places in deathplace:
    if isinstance(places, list):
        for place in places:
            place = place.lower()
            if place in deathcount:
                deathcount[place] += 1
                if deathcount[place] >= 10:
                    final_deathcount[place] = deathcount[place]
            else:
                deathcount[place] = 1
    else:
        if places in deathcount:
            places = places.lower()
            deathcount[places] += 1
            if deathcount[places] >= 10:
                    final_deathcount[places] = deathcount[places]
        else:
            deathcount[places] = 1



print(final_deathcount)