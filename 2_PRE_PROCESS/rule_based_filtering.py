# Load Modules
import pandas as pd
import spacy
import string

# Load Pre-Trained Language Model from spaCy
nlp = spacy.load('en_core_web_md')

# Load title collection of Reddit
df = pd.read_csv('../0_DATA/raw/reddit_titles_cleaned.csv')


# --- Rule-Based Filtering : Remove duplicates
df = df.drop_duplicates()


# --- Rule-Based Filtering : Remove sentence with 3 words or shorter
df = df[df.apply(lambda x: len(x.split(' ')) > 3)]


# Initiate the Doc-Objects
df = df.apply(lambda x: nlp(x))


# --- Rule-Based Filtering : Check if token has no vector
def contains_no_vector(x):
    return False not in [token.has_vector for token in x]

df = df[df.apply(contains_no_vector)]


# --- Rule-Based Filtering : Check if root exists
def contains_root(x): 
    return 'ROOT' in [token.dep_ for token in x]

df = df[df.apply(contains_root)]


# --- Rule-Based Filtering : Check if subject exists
def check_subject(x):
    dep = [token.dep_ for token in x]
    return any('subj' in tag for tag in dep)

df = df[df.apply(check_subject)]


# --- Rule-Based Filtering : Check if not one pos-tag is dominating
def check_pos_distribution(x): 
    pos = [token.pos_ for token in x]
    pos_dict = {i:pos.count(i) for i in pos}
    for tag in pos_dict:
        if pos_dict[tag] >= (len(pos) * 0.8):
            return False
    return True

df = df[df.apply(check_pos_distribution)]


# --- Rule-Based Filtering : Check if root == verb / adverb
def check_root(x):
    pos = [token.pos_ for token in x]
    dep = [token.dep_ for token in x]
    return pos[dep.index('ROOT')] in ['VERB', 'ADV']

df = df[df.apply(check_root)]


# write to csv
df = df.apply(lambda x: " ".join([token.text for token in x]))
df.to_csv('../0_DATA/raw/reddit_titles_filtered.csv')