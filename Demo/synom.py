import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()

    # Retrieve synonyms from WordNet
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  # Add synonym to the set

    return list(synonyms)
