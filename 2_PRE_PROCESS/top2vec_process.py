# Load Modules
import pandas as pd
import spacy

# Load Pre-Trained Language Model from spaCy
nlp = spacy.load('en_core_web_md')


# Load title collection of Reddit
df = pd.read_csv('../0_DATA/raw/reddit_titles_filtered.csv')


# Initiate the Doc-Objects
df = df.apply(lambda x: nlp(x))


# Only get keywords from the text
def get_keywords(x):
    result = []
    
    pos = [token.pos_ for token in x]
    dep = [token.dep_ for token in x]
    for index, token in enumerate(x):
        if pos[index] in ['VERB', 'ADV', 'NOUN', 'PROPN', 'ADJ'] or dep[index] in ['ROOT', 'subj', 'obj']:
            result.append(token)
    return result
    
df = df.apply(get_keywords)


# Lemmatizing the remaining words
df = df.apply(lambda x: " ".join([token.lemma_ for token in x]))


# write to csv
df = pd.to_csv('../0_DATA/raw/reddit_titles_top2vec.csv')