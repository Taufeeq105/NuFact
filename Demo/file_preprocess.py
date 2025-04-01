import requests


#inp = hold[0]

def preprocess(inp):
    query = inp['sentence'][0]
    sents = [s for s in inp['proof'] if "http" not in s]
    urls = list([s for s in inp['proof'] if "http" in s])
    #urls = list(set([s for s in inp['proof'] if "http" in s]))
    ents = inp['entity'][0]
    #ents = [inp['quantity_1']['entityStr']][0]
    return query,sents,urls,ents

#def preprocess(inp):
#    query = inp['sentence']
#    sents = {query:[s for s in inp['proof'] if "http" not in s]}
#    urls = {query: list(set([s for s in inp['proof'] if "http" in s]))}
#    ents = [inp['quantity_1']['entityStr']]
#    return query,sents,urls,ents
