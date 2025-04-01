import google.generativeai as genai
import os
import json
import time
import requests
import asyncio
from asypage import fetch_multiple_webpages
from bs4 import BeautifulSoup

genai.configure(api_key='add yours')
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

async def asynctxt(urls):
    results = await fetch_multiple_webpages(urls)
    return {url: text for url, text in results}  # Convert list of tuples to dict

def get_webpage_texts(urls):
    return asyncio.run(asynctxt(urls))
    
#webpage_texts = get_webpage_texts(urls)      

def trustworthiness(query, webpage_text):
    prompt = f"""
    Your task is to assess the trustworthiness of a webpage based on its content and a specific query.
    Start by examining how well the webpage text aligns with the query, focusing on the accuracy and relevance of the information.
    Consider whether the content thoroughly addresses the key topics related to the query.
    Based on this evaluation, determine how trustworthy the webpage is in providing accurate and reliable information related to the query.
    If the webpage is trustworthy then return 1 else 0. NO OTHER EXPLAINATION REQUIRED

    Query: {query}

    Webpage Text: {webpage_text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()
 
# webpage_texts is a dictionary whose key is url and value is its webpage text  
  
def trustworthiness_all(query,webpage_texts):
    rm = []
    for i,j in webpage_texts.items():
        if len(j)>5:
            rm.append(int(trustworthiness(query, j)))
            time.sleep(3)
    if len(rm)>0:
        return sum(rm)/len(rm)
    else:
        return 0
        
def title_trust(query,url):
  prompt = (
    f"I have a specific query and a URL, and I need to determine if this URL is likely to be relevant "
    f"to the query based on its structure and keywords. "
    f"if you think it is relevant return 1 else 0. NO OTHER EXPLAINATION REQUIRED"
    f"Query: {query} "
    f"URL: {url} "
  )
  response = model.generate_content(prompt)
  return response.text.strip()
  
def LLM_decision(query, sentences):
    prompt = f"""
    Read the Query and proof sentences.
    Based on the proof sentences, make a decision on whether the Query is true or not. If true, return 1; otherwise, return 0. NO OTHER EXPLANATION REQUIRED.

    Query:
    {query}

    Sentences:
    {sentences}
    """
    response = model.generate_content(prompt)
    return response.text.strip()
    
def title_trust_all(query,q,urls):
    uls = urls
    rm = []
    for i in uls:
        rm.append(int(title_trust(query,i)))
        time.sleep(3)
    return sum(rm)/len(rm)
    
    
    
