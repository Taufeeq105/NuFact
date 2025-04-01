# # Mine
# api_key1 = 'AIzaSyDaNPgf0eGrh8kzHc-pA88u1lJSB1WDdK0' # paid
# cse_id1 = '900dcf0e5ff9f4ecb'
# #Dandriyal
# api_key1 = 'AIzaSyBujtADqXJR_yibuVbKWGteVhDUesFh4ek'
# cse_id1 = '233e0cf4f93414b26'
from googleapiclient.discovery import build
import requests
import json
import time

def google_search(query, num_results=40):
    # Your API key and Custom Search Engine ID
    # Nitesh
    api_key1 = 'AIzaSyCnuXqAnbOTjKjqPWJCKULhYQEyyhkqW4s'    
    cse_id1 = 'd77e04c600b184862'
    api_key = api_key1
    cse_id = cse_id1
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
    hold = all_results[:num_results]
    soldat = []
    for i in range(len(hold)):
        soldat.append(hold[i]['link'])
    soldat = [link for link in soldat if not link.lower().endswith('.pdf')]
    soldat = [link for link in soldat if not link.lower().endswith('.asp')]
    return soldat

