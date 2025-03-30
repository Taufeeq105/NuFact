import re
import json
import pandas as pd
import json
import random
from bs4 import BeautifulSoup
import re
import requests
import time
import math
import os
import pandas as pd

column_names=['sent1','sent2','sent3','trust1','trust2','trust3']
df = pd.DataFrame(columns=column_names)
dummy=[0 for i in range(6)]
df.loc[0]=dummy

txt='/content/sample_data/sample.txt'
txt1='/content/sample_data/output0-50.txt'
folder='/content/drive/MyDrive/MS_Project/dataset/factcheck/'

file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

file_names

with open(txt, 'r') as file:
    # Read the entire content of the file
    file_content = file.read()

def rdfile(content):
  result=[]
  temp=content.split('++++++++++++query+++++++++++++++')[1:]
  for i in temp:
    pr=i.split('+++++++++++++++++++++++++++')[1:]
    # print(pr)
    for j in pr:
      prin=j.split('\n')
      if len(prin[2])>0 and len(prin[3])>0: #empty results
        # print(prin[2:])
        result.append(prin[2:])
  return result

# turs=rdfile(file_content)

def data(files):
  for i in files:
    path=folder+i
    with open(path, 'r') as file:
      file_content = file.read()
    turs=rdfile(file_content)
    sent=[]
    trust=[]
    for k in range(len(turs)):
      stat=[]
      scr=[]
      for l in range(len(turs[k])):
        if 'trustworthiness' in turs[k][l]:
          stat.append(turs[k][l-1])
          if turs[k][l].split(':')[1]=='NaN' :
            continue
          scr.append(turs[k][l].split(':')[1])
          if len(scr)==3:
            break
      if len(scr)>0:
        sent.append(stat)
        trust.append(scr)
    for i in range(len(sent)):
      tmp=sent[i]+list(map(lambda x: round(float(x), 3),trust[i]))
      if len(tmp)<6:
        continue
      df.loc[len(df)]=tmp
  return df

dataset=data(file_names)

dataset.tail()

len(tmp)

dummy=[0 for i in range(6)]

dummy

df.loc[0]=dummy

# Append the data to the DataFrame
for i in range(len(sent)):
  tmp=sent[i]+list(map(lambda x: round(float(x), 3),trust[i]))
  if len(tmp)<6:
    continue
  df.loc[len(df)]=tmp

temp=file_content.split('++++++++++++query+++++++++++++++')[1:]
temp[8].split('+++++++++++++++++++++++++++')[1]
