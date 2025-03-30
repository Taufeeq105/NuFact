pip install -U sentence-transformers

import re
import json
import pandas as pd
import random
import time
import math
import os

ROUND_BRACKETS = re.compile(r'\(.+?\)')
SQUARED_BRACKETS = re.compile(r'\[.+?\]')
TRASH = re.compile(r'[^a-zA-Z0-9.?!\' ]')
WHITESPACES = re.compile(r'\n')
DOUBLE_WHITESPACES = re.compile(r'\s+')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from afinn import Afinn
from sentence_transformers import SentenceTransformer
import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset

sbert = SentenceTransformer('stsb-roberta-base-v2')

import torch.nn as nn
import torch.optim as optim

column_names=['sent1','sent2','sent3','trust1','trust2','trust3']
df = pd.DataFrame(columns=column_names)
dummy=[0 for i in range(6)]
df.loc[0]=dummy

# folder='/content/drive/MyDrive/MS_Project/dataset/factcheck/'
folder = '/content/drive/MyDrive/MS_Project/dataset/factcheck_my/'
file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

# file_names = file_names[2:]
path1 = '/content/drive/MyDrive/MS_Project/dataset/factcheck_my/test_data/csv/testneg (1).csv'
path2 = '/content/drive/MyDrive/MS_Project/dataset/factcheck_my/test_data/csv/factcheck_testdata_embeddings_true.csv'

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)

file_names

"""# data load"""

def replace_patterns(input_text):
    # Replace occurrences of patterns
    result = ROUND_BRACKETS.sub('', input_text)
    result = SQUARED_BRACKETS.sub('', result)
    result = TRASH.sub('', result)
    result = WHITESPACES.sub('', result).strip()
    result = DOUBLE_WHITESPACES.sub(' ', result).strip()
    return result

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

dataset

dataset.drop(0, inplace=True)

len(dataset)

dataset['sent1'] = dataset['sent1'].apply(lambda x: replace_patterns(x))
dataset['sent2'] = dataset['sent2'].apply(lambda x: replace_patterns(x))
dataset['sent3'] = dataset['sent3'].apply(lambda x: replace_patterns(x))

dataset = df1.copy()

#Test data out

def transform(x):
  embeddings = sbert.encode(x)
  # embed = embeddings.ToTensor()
  return embeddings

dataset['sent1'] = dataset['sent1'].apply(lambda x: transform(x))
dataset['sent2'] = dataset['sent2'].apply(lambda x: transform(x))
dataset['sent3'] = dataset['sent3'].apply(lambda x: transform(x))

dataset.isnull().sum()

# dataset.to_csv('test_data_factcheck_embedding.csv', index=False)

dataset.head()

len(dataset)

dataset.to_csv('train_numeral_hybrid.csv')

num_columns = 2307
column_names = [f'z{i+1}' for i in range(num_columns)]
df = pd.DataFrame(columns=column_names)

dataset.iloc[0]['sent1']

# unpacking those lists

for i in range(len(dataset)):
  a,b,c=dataset.iloc[i]['trust1'],dataset.iloc[i]['trust2'],dataset.iloc[i]['trust3']
  trust=[]
  trust.extend([a,b,c])
  dt=list(dataset.iloc[i]['sent1'])+list(dataset.iloc[i]['sent2'])+list(dataset.iloc[i]['sent3'])
  f=dt+trust
  df.loc[i]=f

df.head()

df.to_csv('train_numeral_hybrid.csv')

"""# train"""

from sklearn.model_selection import train_test_split

path = '/content/drive/MyDrive/MS_Project/dataset/hybridfc_text_data/hybridfc_text_embedding.csv'
dtrain = pd.read_csv(path,index_col=0)

label = dtrain['z2308']
dtrain['label'] = label
dtrain.drop(['z2308'],inplace=True,axis=1)

y = dtrain['label']
X = dtrain.drop(['label'],axis=1)
X.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

train = TensorDataset(torch.Tensor(np.array(X_train)), torch.Tensor(np.array(y_train)))
train_loader = DataLoader(train, batch_size = 10, shuffle = True)

test_X = torch.tensor(X_test.to_numpy(dtype=np.float32), dtype=torch.float32)
test_y = torch.tensor(y_test.to_numpy(dtype=np.float32).reshape(-1, 1), dtype=torch.float32)

test_X[0].shape

len(train)

sentence_dim=768*3+3
shallom_width=512
# loss = torch.nn.BCELoss()

sentence_dim

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        # Define image classification layers
        self.image_classification_layer = nn.Sequential(
            nn.Linear(2307, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.50),
            nn.Linear(512, 512)
        )

        # Define final classification layer
        self.final_classification_layer = nn.Sequential(
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.50),
            nn.Linear(512, 1)
        )

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten the input image tensor
        image_embedding = self.image_classification_layer(x)
        z = torch.cat([image_embedding], 1)
        return torch.sigmoid(self.final_classification_layer(z))

model = NeuralNetwork()
criteria = nn.BCELoss()  # Assuming binary classification
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5

for epoch in range(epochs):
    for batch_X, batch_y in train_loader:
        outputs = model(batch_X)
        batch_y = batch_y.view(-1, 1)
        loss = criteria(outputs, batch_y.float())  # Assuming binary classification
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

model.eval()

y_pred = model(test_X)

acc = (y_pred.round() == test_y).float().mean()

acc = float(acc)
print("Model accuracy: %.2f%%" % (acc*100))
