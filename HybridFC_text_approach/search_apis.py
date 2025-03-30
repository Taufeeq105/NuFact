from googleapiclient.discovery import build
import requests
import json
import time


api_key = ''
cse_id = ''

pth='/content/sample_data/2216qrs.json'

with open(pth,'r') as json_file:
  tmp=[json.loads(line) for line in json_file]  #loading json

# def google_search(query):
#     service = build("customsearch", "v1", developerKey=api_key)
#     result = service.cse().list(q=query, cx=cse_id).execute()
#     return result['items']

def google_search(query, num_results=40):
    # Your API key and Custom Search Engine ID
    api_key = '' #dandriyal
    cse_id = ''
    service = build("customsearch", "v1", developerKey=api_key)
    start_index = 1
    all_results = []
    while len(all_results) < num_results:
        result = service.cse().list(q=query, cx=cse_id, start=start_index).execute()
        items = result.get('items', [])
        all_results.extend(items)
        if not result.get('queries', {}).get('nextPage'):
            break
        start_index += 10  # The API returns up to 10 results per request
    return all_results[:num_results]


len(tmp)

var=0
for pm in range(2000,2216):
  try:
      soldat=[]
      # pr=data[pm][list(filter(lambda x: 'sentence' in x, list(data[pm].keys())))[0]]
      pr=tmp[pm]['sentence']
      # print(pr)
      results = google_search(pr)
      for i in range(len(results)):
        soldat.append(results[i]['link'])
      tmp[pm]['links']=soldat
      time.sleep(3)
      # var+=1
      # if var==50:
      #   break
  except:
    continue

tmp[2213]

len(tmp)



opo='/content/drive/MyDrive/MS_Project/dataset/query and links/1580linksres.json'
with open(opo,'r') as json_file:
  data2=[json.loads(line) for line in json_file]

len(data2)

res=data2+tmp

len(res)

res[3777]

for l in range(80,len(tmp)):
  print(tmp[l])

with open('2216linksres.json', 'w') as file:  #saving json
  for e in tmp:
    json.dump(e, file)
    file.write('\n')

# Example usage
# search_query = 'Tanzania Population'
# results = google_search(search_query)

for result in results:
    print(f"Title: {result['title']}\nLink: {result['link']}\n\n")

results[0]['link']

for i in range(len(results)):
  print(results[i]['link'])

def geturls(query) :
  subscription_key = ""
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

geturls('Krupp Factory')
