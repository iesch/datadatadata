import json

# load the data
with open('People/A_people.json') as file:
    data = json.load(file)

# initialize variables
deathplace = []
deathcount = {}
final_deathcount = {}

# filter for only entries that include death place
for dict in data: 
    if 'ontology/deathPlace_label' in dict:
        deathplace.append(dict['ontology/deathPlace_label'])

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