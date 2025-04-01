from py_heideltime import heideltime
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import spacy
from sentence_transformers import SentenceTransformer
import re
import pandas as pd
import random
import time
import math
import os
import json
import numpy as np
from datetime import *
from dateutil.parser import *
from quantulum3 import parser

nlp = spacy.load("en_core_web_sm")
sbert = SentenceTransformer('stsb-roberta-base-v2')

def transform(x):
  embeddings = sbert.encode(x)
  return embeddings
  
def semantic(sents,query):
    emb_q = transform(query)
    embedd = transform(sents)
    similarities = sbert.similarity(embedd,emb_q)
    tmp = np.array(similarities).tolist()
    flat_list = [item[0] for item in tmp]
    return flat_list,sum(flat_list) / len(flat_list)
    
def relevant_sent(sents,query):
    arr = semantic(sents,query)
    indx = [x for x in range(len(arr[0])) if arr[0][x] > 0.5]
    relevants = [sents[i] for i in indx]
    return relevants
    
def calculate_z_score(sents,query):
    avg = []
    sents = relevant_sent(sents,query)
    for i in sents:
        quants = parser.parse(i)
        avg+=[j.value for j in quants]
    avg = list(filter(lambda x: not (1900 <= x <= 2100), avg))
    mean = np.mean(avg)
    std_dev = np.std(avg)
    # z = [f for f in avg if abs((f - mean) / std_dev)<1]
    z = [abs((f - mean) / std_dev) for f in avg]
    # z_score = (fact - mean) / std_dev
    return z,avg#,mean,std_dev
    
def round_number(number):
    base = 10 ** (len(str(int(number))) - 1)
    up = (int(str(number)[0])+1)*base
    down = (int(str(number)[0])-1)*base
    return up,down,base  #,round(number / base) * base
    
def ten_percent(lst,query_quant):
    error = query_quant*0.1
    up = query_quant + error
    down = query_quant - error
    final = [b for b in lst if down <= b <= up]
    return final

def calculate_quantity_score(sents,query):
    avg = []
    qr = []
    sents = relevant_sent(sents,query)
    query_quants = parser.parse(query)
    qr+=[k.value for k in query_quants]
    qr = list(filter(lambda x: not (1900 <= x <= 2100), qr))[0]
    up,down,d = round_number(qr)
    for i in sents:
        quants = parser.parse(i)
        avg+=[j.value for j in quants]
    avg = list(filter(lambda x: not (1900 <= x <= 2100), avg))
    final = [b for b in avg if down <= b <= up]
    final = ten_percent(final,qr)
    print('query quant ===>',qr,'proof sentence qunat ===>',avg,'final ===>',final)
    verdict = len(final)>2
    return final

def sentence_contain_quant_tolerance(sents,query):
    avg = []
    qr = []
    query_quants = parser.parse(query)
    qr+=[k.value for k in query_quants]
    qr = list(filter(lambda x: not (1900 <= x <= 2100), qr))[0]
    up,down,d = round_number(qr)
    cnt = 0
    for i in sents:
        quants = parser.parse(i)
        avg = [j.value for j in quants]
        avg = list(filter(lambda x: not (1900 <= x <= 2100), avg))
        final = [b for b in avg if down <= b <= up]
        final = ten_percent(final,qr)
        if len(final)>0:
            cnt+=1
    return cnt
    
def temporal_similarity(query,sent_tagged):
    tmp1 = time(query)
    feature = sum([sent_tagged.count(i) for i in tmp1])
    return feature #,tmp2
    
def sent_tag(sent):
    lst = []
    for s in sent:
        val2 = time(s)
        lst.extend(val2)
    return lst
    
def temp_agreement(sent_tagged):
    out = [k for k in sent_tagged if k!='PRESENT_REF']
    x = len(out)
    y = len(list(set(out)))
    return (x-y)+1

def calculate_quant_presence_score(query,sents):
    query_quants = parser.parse(query)
    qr = []
    qr+=[k.value for k in query_quants]
    qr = list(filter(lambda x: not (1900 <= x <= 2100), qr))
    avg = []
    for i in sents:
        quants = parser.parse(i)
        avg+=[j.value for j in quants]
    avg = list(filter(lambda x: not (1900 <= x <= 2100), avg))
    #print(avg)
    feature = sum([avg.count(i) for i in qr])
    return feature
    
def calculate_quant_agreement(sents):
    avg = []
    for i in sents:
        quants = parser.parse(i)
        avg+=[j.value for j in quants]
    avg = list(filter(lambda x: not (1900 <= x <= 2100), avg))
    x = len(avg)
    y = len(list(set(avg)))
    return (x-y)+1

def temp_trust(sents,entity):
    base = "https://en.wikipedia.org/wiki/"
    txt = get_paragraph_text(base+entity)
    b = time(txt)
    incr = 0
    for i in sents:
        feature = sum([b.count(i) for i in sents if i!='PRESENT_REF'])
        if feature!=0:
           incr+=1
    return incr/len(sents)
    
def get_paragraph_text(url):
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraph_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return paragraph_text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return ""
        
def time(s):
    timexs = heideltime(s,language='English',document_type='news',dct='1939-08-31')
    return [i['value'] for i in timexs] #timexs,    
    
    

