from flask import Flask, request, jsonify, render_template, redirect, url_for
import google.generativeai as genai
import json
import subprocess
import time
import math
import torch
import spacy
import warnings
import webbrowser
from synom import get_synonyms
from api_call import google_search
from feature_vect import feature_compute
from file_preprocess import preprocess
from features import sent_tag
from gemini import get_webpage_texts
from model import NeuralNetwork  
#
warnings.filterwarnings('ignore')

genai.configure(api_key='add yours')
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

proof_data = {}  # Global dictionary to store proof results

def gensens(subject, relation, object_, quantity):
    prompt = f"""
    Given the following structured input, generate a well-formed quantitative assertion.

    Subject: {subject}
    Relation: {relation}
    Object: {object_}
    Quantity: {quantity}

    Construct the assertion in a natural sentence format, and return only the sentence with no other explanation required.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

def extract_subject_verb(sentence):
    doc = nlp(sentence)
    subject = None
    verb = None
    
    for token in doc:
        if token.dep_ == "nsubj":  # Extract subject
            subject = token.text
        if token.dep_ == "ROOT":  # Extract main verb
            verb = token.text
            
    return subject, verb

def open_url(url):
  try:
    webbrowser.open_new_tab(url)  # Opens in a new tab if possible
    print(f"Opened URL: {url}")
  except webbrowser.Error as e:
    print(f"Error opening URL: {e}")
  except Exception as generic_error:
    print(f"An unexpected error occured: {generic_error}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_assertion():
    global proof_data

    data = request.json  # Ensure data is extracted from request

    if "statement" in data:
        assertion = data["statement"].strip()  # Ensure statement is properly formatted
        subject, relation = extract_subject_verb(assertion)
        object_ = "doesn't matter"

    else:
        subject = data.get("subject", "").capitalize().strip()
        relation = data.get("relation", "").strip()
        object_ = data.get("object", "").strip()
        quantity = data.get("quantity", "").strip()

        if not (subject and relation and object_ and quantity):
            return jsonify({"error": "All fields are required"}), 400

        assertion = gensens(subject, relation, object_, quantity)  # Generate assertion
    print("inurl:wiki "+assertion)
    urls = google_search(assertion)

    predicates = get_synonyms(relation)
    predicates = list(filter(lambda x: x.count('_') < 2, predicates))
    predicates = list(map(lambda x: x.replace('_', ' '), predicates))

    dct = {
        "subject": subject.capitalize(),
        "predicate": relation,
        "object": object_,
        "sentence": assertion,
        "links": urls,
        "base_pred": predicates
    }

    # Save assertion data to JSON
    with open("/home/user/Desktop/demo/d1.json", "w") as file:
        json.dump([dct], file, indent=4)

    # Run Java process
    process = subprocess.Popen(["gnome-terminal", "--", "java", "-jar", "/home/user/udemy/out/artifacts/udemy_jar/udemy.jar"])
    process.wait()
    time.sleep(40)

    # Load proof data
    path = '/home/user/Pictures/proofs.json'
    with open(path, "r") as f:
        data = json.load(f)

    query, sents, urls, ent = preprocess(data)
    print(len(sents),len(query),len(urls))
    webpage_texts = get_webpage_texts(urls)
    tagged = sent_tag(sents)
    vector = feature_compute(query, sents, urls, ent, tagged, webpage_texts)
    print(vector)
    # Load trained model
    model = NeuralNetwork()
    model.load_state_dict(torch.load("/home/user/Pictures/paper/model.pth", map_location=torch.device('cpu')))
    model.eval()
    
    with torch.no_grad():
        vect = torch.tensor(vector, dtype=torch.float32)  # Convert list to tensor
        vect = vect.view(1, -1)  # Reshape if needed
        logits = model(vect)  # Get raw scores
        score = torch.sigmoid(logits)  # Apply sigmoid activation
        #score = model.predict(vector)

    print("Score:", score)

    feature_names = [
        "Semantic Similarity Average", "No. of Relevant Sentences", "No. of Quantities under tolerance",
        "No. of Sentences which have Quantity under tolerance", "Temporal Similarity", "Temporal Trustworthiness",
        "Hit Count", "Quantitative Coherence among proofs", "Temporal Coherence among proofs", 
        "Prompt 1", "Prompt 2", "Prompt 3"
    ]
    d = dict(zip(sents,urls))
    result = [item for pair in d.items() for item in pair]
    print(result)
    # Store proof data globally
    if math.trunc(score.item() * 100) / 100 > 0.51:
        print('enter with more than 0.5')
        proof_data = {
            "assertion": assertion,
            "score": f"True  ({score.item():.4f})",
            "proof": result, 
            #"urls": urls,
            "entities": ent,
            "vector": vector,
            "feature_names": feature_names
        }
    elif math.trunc(score.item() * 100) / 100 <= 0.50:
        print('entered with less than 0.5')
        proof_data = {
            "assertion": assertion,
            "score": f"False  ({score.item():.4f})",
            "proof": result,
            #"urls": ["no supporting doc"],
            "entities": ent,
            "vector": vector,
            "feature_names": feature_names
        }
    with open('/home/user/Desktop/demo/datadis.json', 'w') as json_file:
         json.dump(proof_data, json_file, indent=4)
    print("All Done")
    print(proof_data)
    print("mani")
    open_url('http://127.0.0.1:5000/proof')
    return redirect(url_for('proof_page'))

@app.route('/proof')
def proof_page():
    #global proof_data
    return render_template('proof.html', proof_data=proof_data)

if __name__ == '__main__':
    app.run(debug=True)

