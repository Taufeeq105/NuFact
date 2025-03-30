import re
import json
import pandas as pd
import json
import random
from bs4 import BeautifulSoup
import re
import spacy
import requests
import time
nlp = spacy.load("en_core_web_sm")

json_path='/content/drive/MyDrive/MS_Project/dataset_with_event_when_temporal_tag_in_context.json'
res='/content/drive/MyDrive/MS_Project/results_plus_json_details.json'

with open(json_path,'r') as json_file:
  data=[json.loads(line) for line in json_file]

items = ["Lambells Lagoon", "BT Broadband", "Openreach", "Openreach", "Openreach", "World Championships",
         "BMA Magazine", "Mos Def", "Carbon Recycling International", "John Barnum", "Montana Freemen", "Mount Kahuzi",
         "Don Cordner", "Tronox", "Tronox", "Chile", "Chile", "Chile", "Chile", "Chile", "Chile", "Chile", "Chile", "Chile",
         "Kitt Peak National Observatory", "Naoto Hikosaka", "Myasishchev", "Anastasia Myskina", "Raška District", "WordPress", "WordPress",
         "Fronde", "Mike Zwerin", "Banco de Venezuela", "Gerald Wickremesooriya", "prototile", "Frances Adaskin", "Brio Superfund site", "MPR",
         "PrisXtra", "Guantánamo", "Bassiknou", "Pelephone", "Pelephone", "WNVA", "KordaMentha", "MOL Group", "Donna Michelle Pope", "Adrian VI",
         "Bank of British West Africa", "Warcino", "mutoscope", "Nundasuchus", "Valletta", "McGregor Lake", "East Kilbride independence referendum",
         "Sinclair Broadcast Group", "Sinclair Broadcast Group", "HBO", "Strath Haven High School", "Frances Lincoln", "Ben Kiernan", "Orcus", "Albanian Armed Forces",
         "Przemysł I", "Oxygen therapy", "William Bankier", "Olympia 66", "Marin County", "Grace Wahu", "Portland Open Invitational", "Sacred Heart", "Lazonby", "FC Basel",
         "FC Basel", "Dasavathaaram", "Al Bidda", "Derek Weiler", "Fife Constabulary", "Calenberg Land", "Krupp", "Sean Chu", "Ganta", "Government of West Bengal", "Faneuil Hall",
         "Changsha", "Changsha", "The Railway Magazine", "NISMART", "Vladimír Klokočka", "William A. Clark", "Phu Thai language", "Boeing", "Bopal", "Ramachandra Vitthala Rao",
         "Zyvex Technologies", "Plaza Hotel", "Plaza Hotel", "Plaza Hotel", "Landmaster", "Hucknall", "Sein Htwa Kanche", "Étretat", "Gujarat", "Gujarat", "Gujarat", "Gujarat", "Gujarat",
         "Gujarat", "Gujarat", "Gujarat", "Oulu", "Oulu", "Britney Spears", "Lausitzer Rundschau", "Nelly", "Kibuku District", "Billstedt", "Billstedt", "Max Näther", "Canal J"]

data[9][list(filter(lambda x: 'sentence' in x, list(data[9].keys())))[0]]

data[0]

len(data)

var=0
for i in data:
  p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]
  if p[:3]=='His' or p[:2]=='He' or p[:3]=='Her' or p[:3]=='She' or p[:4]=='They':
    data.pop(var)
  var+=1

len(data)

for i in data:
  p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]
  if 'one of the bombings' in p:
    print(p)

var=0
for i in data:
  p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]
  qstr=i['quantity_1']['quantityStr']
  if 'several' in qstr:
    data.pop(var)
  var+=1

len(data) # total estimate die

"""Unique entity"""

ents=[]
snts=[]
for i in data:
  k=i['quantity_1']['entityStr']
  if k not in ents:
    ents.append(k)
    snts.append(i)

len(snts)

for i in snts:
  p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]
  if ' rate' in p:
    print(p)

var=[]
for i in snts:
  p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]
  if ' total' in p:
    # print(p)
    var.append(i)
  if ' estimate' in p:
    # print(p)
    var.append(i)
  if ' die' in p:
    # print(p)
    var.append(i)
  if ' rate' in p:
    # print(p)
    var.append(i)

len(var)

var[45]

with open('useful.json', 'w') as file:  #saving json
  for e in var:
    json.dump(e, file)
    file.write('\n')

# def pred(my_list, my_string):
#     for element in my_list:
#         if element in my_string:
#             return True
#     return False

# with open('output_numeral.txt', 'w') as file:
#     for i in st:
#         file.write(i + '\n')

"""purchase predicate optional"""

# purchase_list=[]
# for k in range(len(data)):
#     # print(data[k][list(data[k].keys())[0]])
#     if "purchase" in data[k][list(data[k].keys())[0]]:
#         purchase_list.append(data[k])

filtered_q1=[]
filtered_q2=[]
filtered_q3=[]
filtered_q4=[]

data[0]

list(data[0].keys())[0]

"""No complex sentence with multiple quantities"""

for i in data:
  # print(len(list(i.keys())))
  if len(list(i.keys())) == 5:
    filtered_q1.append(i)
  elif len(list(i.keys())) == 6:
    filtered_q2.append(i)
  elif len(list(i.keys())) == 7:
    filtered_q3.append(i)
  elif len(list(i.keys())) == 8:
    filtered_q4.append(i)
  # print(i['Event'])

df=data[:50]

len(filtered_q1)

lst=[]
lst_not=[]

filtered_q1[0]['quantity_1']['entityStr']

"""Entity Should be correct"""

filtered=[]
for i in range(len(filtered_q1)):
  # op=filtered_q1[i][list(filter(lambda x:'quantity' in x,list(filtered_q1[i].keys())))[0]]['context']
  enty=filtered_q1[i]['quantity_1']['entityStr']
  doc = nlp(enty)
  for ent in doc.ents:
    if ent.label_ not in ['DATE','QUANTITY','PERCENT','ORDINAL','CARDINAL','MONEY','TIME']:
      # print(ent.text, ent.label_)
      filtered.append(filtered_q1[i])

len(filtered)

"""Quantity should have numeral"""

numeral_pattern = re.compile(r'\d+') #quantity contains at least one numeral

more_filtered=[]

for i in range(len(filtered)):
  # op=filtered_q1[i][list(filter(lambda x:'quantity' in x,list(filtered_q1[i].keys())))[0]]['context']
  qnty=filtered[i]['quantity_1']['quantityStr']
  if bool(numeral_pattern.search(qnty)):
    more_filtered.append(filtered[i])
  # print(qnty)

len(more_filtered)

"""quantity should not be time"""

year_pattern = re.compile(r'\b(?:19\d\d|20[0-1]\d|202[0-3])\b')

more_more_filtered=[]

for i in range(len(more_filtered)):
  # op=filtered_q1[i][list(filter(lambda x:'quantity' in x,list(filtered_q1[i].keys())))[0]]['context']
  qnty=more_filtered[i]['quantity_1']['quantityStr']
  if not bool(year_pattern.search(qnty)):
    more_more_filtered.append(more_filtered[i])
    print(qnty)

len(more_more_filtered)

more_more_filtered[0]

len(more_more_filtered)

clutter_free=[]

for l in range(len(more_more_filtered)):
  p=more_more_filtered[l-1][list(filter(lambda x: 'sentence' in x, list(more_more_filtered[l-1].keys())))[0]]
  q=more_more_filtered[l][list(filter(lambda x: 'sentence' in x, list(more_more_filtered[l].keys())))[0]]
  if p[:10]==q[:10]:
    continue
  # print(p[:15])
  clutter_free.append(more_more_filtered[l])

len(clutter_free)

snts=[]
for k in clutter_free:
  pp=k[list(filter(lambda x: 'sentence' in x, list(k.keys())))[0]]
  snts.append(pp)

snts

with open('dump4150.txt', 'w') as file: # writing sentences in txt file
    for i in snts:
        file.write(i + '\n')

# p=i[list(filter(lambda x: 'sentence' in x, list(i.keys())))[0]]

"""# Removing Duplicates"""

filtered = filter(lambda x: 'sentence' in x, list(more_more_filtered[90].keys()))
filtered_list = list(filtered)

filtered_list

ajm=[]
df=[]
for j in more_more_filtered:
  key = list(filter(lambda x: 'sentence' in x, list(j.keys())))
  sn=j[key[0]]
  if sn not in ajm:
    ajm.append(sn)
    df.append(j)

len(ajm)

len(df)

pip install jsonlines

import jsonlines

json_path = "df.jsonl"

with jsonlines.open(json_path, 'w') as json_file:
    json_file.write_all(df)

df

"""filter based on entity"""

entities=[]
quantities=[]
entyfiltered=[]

for j in df:
  if j['quantity_1']['entityStr'] not in entities:
    entities.append(j['quantity_1']['entityStr'])
  # print(j['quantity_1']['entityStr'])

len(entities) # less because duplicates removed

len(entities)

"""# Checking if entity available on dbpedia or not"""

baseurl='https://en.wikipedia.org/wiki/'
dbpedia='https://dbpedia.org/page/'

def check_webpage_existence(url):
    try:
        response = requests.head(url)
        # Check if the status code is in the 2xx range (indicating success)
        return response.status_code // 100 == 2
    except requests.RequestException:
        return False

# Replace 'your_url_here' with the actual URL you want to check
url_to_check = 'your_url_here'

if check_webpage_existence(url_to_check):
    print(f"The webpage at {url_to_check} exists.")
else:
    print(f"The webpage at {url_to_check} does not exist or cannot be reached.")

entities[:100]

entity_with_surface=[]

for kp in entities:
  if check_webpage_existence(dbpedia+kp):
    # print(f"The webpage at {url_to_check} exists.")
    entity_with_surface.append(kp)
  else:
      # print(f"The webpage at {dbpedia+kp} does not exist or cannot be reached.")
      pass
  time.sleep(2)

len(entity_with_surface)

url = ''
# Make an HTTP request to the URL
response = requests.get(dbpedia+'Guantánamo')

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements with rev="dbo:wikiPageRedirects"
    redirect_elements = soup.find_all('a', {'rev': 'dbo:wikiPageRedirects'})

    # Extract and print the redirect links
    redirects = [element['href'] for element in redirect_elements]
    for redirect in redirects:
        print(redirect)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")

# redirects[0].split('/')[-1]
for k in redirects:
  print(k.split('/')[-1])







