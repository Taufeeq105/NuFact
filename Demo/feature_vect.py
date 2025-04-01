from googleapiclient.discovery import build
import requests
import json
import os
import time
import warnings
warnings.filterwarnings("ignore")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from gemini import LLM_decision
from gemini import trustworthiness_all
from gemini import title_trust_all
from features import semantic
from features import relevant_sent
from features import calculate_quantity_score
from features import temporal_similarity
from features import calculate_quant_presence_score
from features import calculate_quant_agreement
from features import temp_agreement
from features import temp_trust
from features import sentence_contain_quant_tolerance

def feature_compute(query,sents,urls,ent,tagged,webpage_texts):
    entity = ent
    start_time = time.time()
    dm1,avg = semantic(sents,query)
    end_time = time.time()
    print("Elapsed Time for semantic average:", end_time - start_time, "seconds")
    start_time = time.time()
    rel_count = len(relevant_sent(sents,query))/len(sents)
    end_time = time.time()
    print("Elapsed Time for sematic relevant count:", end_time - start_time, "seconds")
    #print(query)
    start_time = time.time()
    qnt_count_tenprcnt = len(calculate_quantity_score(sents,query))
    end_time = time.time()
    print("Elapsed Time for qnt_count_tenprcnt:", end_time - start_time, "seconds")
    start_time = time.time()
    temporal_sim_qs = temporal_similarity(query,tagged)
    end_time = time.time()
    print("Elapsed Time for temporal_similarity:", end_time - start_time, "seconds")
    start_time = time.time()
    no_of_sentence_have_quant = sentence_contain_quant_tolerance(sents,query)
    end_time = time.time()
    print("Elapsed Time for no_of_sentence_have_quant:", end_time - start_time, "seconds")
    start_time = time.time()
    llm_dec = int(LLM_decision(query,sents))
    end_time = time.time()
    print("Elapsed Time for LLM_decision:", end_time - start_time, "seconds")
    start_time = time.time()
    titles = title_trust_all(query,query,urls)
    end_time = time.time()
    print("Elapsed Time for title_trust_all:", end_time - start_time, "seconds")
    start_time = time.time()
    trust = trustworthiness_all(query,webpage_texts)
    end_time = time.time()
    print("Elapsed Time for trustworthiness_all:", end_time - start_time, "seconds")
    start_time = time.time()
    trust_temporal = temp_trust(tagged,entity)
    end_time = time.time()
    print("Elapsed Time for temp_trust:", end_time - start_time, "seconds")
    start_time = time.time()
    count_presence = calculate_quant_presence_score(query,sents)
    end_time = time.time()
    print("Elapsed Time for calculate_quant_presence_score:", end_time - start_time, "seconds")
    start_time = time.time()
    count_agree = calculate_quant_agreement(sents)
    end_time = time.time()
    print("Elapsed Time for calculate_quant_agreement:", end_time - start_time, "seconds")
    start_time = time.time()
    temporal_agree = temp_agreement(tagged)
    end_time = time.time()
    print("Elapsed Time for temp_agreement:", end_time - start_time, "seconds")
    prn = [avg,rel_count,qnt_count_tenprcnt,no_of_sentence_have_quant,temporal_sim_qs,
          trust_temporal,count_presence,count_agree,temporal_agree,llm_dec,titles,trust]
    return prn
    
    
    
