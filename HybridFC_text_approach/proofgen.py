# pip install stanza
# import stanza
# stanza.download('en')
# nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos')

import requests
import collections
from bs4 import BeautifulSoup
import pandas as pd
import json

json_path='/content/drive/MyDrive/MS_Project/dataset_with_event_when_temporal_tag_in_context.json'

with open(json_path,'r') as json_file:
  data=[json.loads(line) for line in json_file]

z=383
len(data)

def quan(x):
  if 'quantity' in x:
    return x

list(filter(quan,list(data[0].keys())))[0]

data[0]

entities=[]

for i in range(len(data)):
  entstr=data[i][list(filter(quan,list(data[i].keys())))[0]]['entityStr']
  entities.append(entstr)

entity=list(set(entities))

entity

pop_list=[]

for k in range(len(data)):
    # print(data[k][list(data[k].keys())[0]])
    if "population" in data[k][list(data[k].keys())[0]]:
        pop_list.append(data[k])

len(pop_list)

pop_list[8]

df.head()

print(data[z]['quantity_1']['entityStr'])
print(data[z]['quantity_1']['quantityStr'])

# queries=list(df['sent'][20:40])

p='/content/drive/MyDrive/MS_Project/proofs/output.txt'


link='https://api.cognitive.microsoft.com/bing/v7.0/search'
link2='https://api.bing.microsoft.com/v7.0/search'

def geturls(query) :
  subscription_key = "PUT YOUR KEY"
  search_url = "https://api.bing.microsoft.com/v7.0/search"
  headers = {"Ocp-Apim-Subscription-Key": subscription_key}
  results=[]
  for i in range(1,6):
    params = {"q": query, "textDecorations": True, "textFormat": "HTML","count":10,"offset":(i-1)*10}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    results.append(search_results)
  urlsl=[]
  for ins in results:
      k=len(ins['webPages']['value'])
      for j in range(k):
        urlsl.append(ins['webPages']['value'][j]['url'])
  return urlsl

geturls('einstein')

import time

for i in range(20):
  n=input('enter index')
  for pl in dct[list(dct.keys())[n]]:
    print(pl)
    print('\n')

# key=[i for i in list(json_objects[0].keys()) if 'sentence' in i][0]
# json_objects[0][[i for i in list(json_objects[0].keys()) if 'sentence' in i][0]]

pop_list[0]

geturls(pop_list[0]['sentence_27'])

for k in range(300,len(pop_list)):
  try:
    query=pop_list[k][[i for i in list(pop_list[k].keys()) if 'sentence' in i][0]]
    urls=geturls(query)
    pop_list[k]['links']=urls
    time.sleep(1)
  except:
    continue

for i in pop_list:
  print(i)

# Open a text file in write mode
with open('output_population.txt', 'w') as f:
    # Write the JSON string to the text file
    f.write(json.dumps(pop_list))

var=0
for i in json_objects:
  print(list(i.keys()))

out93=list(filter(lambda x:'links' in list(x.keys()),json_objects))

len(out93)

out93[0]

# Open a text file in write mode
with open('output_hybrid.txt', 'w') as f:
    # Write the JSON string to the text file
    f.write(json.dumps(json_objects))

file_path = "output50.txt"

# data[queries[9]]

def extract_text_from_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            extracted_text = '\n'.join([p.get_text() for p in paragraphs])
            return extracted_text
        else:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def printproof(url,index):
  contxt=pop_list_filtered[index][list(pop_list_filtered[index].keys())[1]]['context']
  path="q"+".txt"
  f=open(path,'a')
  # f.truncate(0)
    # print(j)
  text=extract_text_from_webpage(url)
  doc = nlp(text)
  # Extract sentences
  sentences = [sentence.text for sentence in doc.sentences]
  proof=[]
  # Print the sentences
  for i, sentence in enumerate(sentences):
    temp=sentence.split()
    matching_tokens = [token for token in temp if token in contxt]
    # synonyms_for_purchase = ["purchase","Buy","Acquire","Procure","Obtain","Get","Secure","Shop for","Acquisition","Possession","Buyout","Procurement","Buying","Gain"] previous
    # any(token in sentence for token in synonyms_for_purchase)
    if len(matching_tokens) > 2 and "purchase" in sentence:
      f.write(f"{i + 1}: {sentence}\n")
      f.write(url + "\n")
      f.write("********************************************\n")
    # if len(matching_tokens)>2 and "purchase" in sentence:
    #   # print(f"Sentence {i + 1}: {sentence}")
    #   f.write(f"{i + 1}: {sentence}")
    #   #  proof.append(sentence)
    #   f.write('\n\n\n')
    #   # print('url ==>',j)
    #   f.write(url)
    #   # print('\n')
    #   f.write('\n\n\n')
    #   # print('*********************************************')
    #   f.write('********************************************')
    #   # print('\n')
    #   f.write('\n\n\n')
  f.close()


