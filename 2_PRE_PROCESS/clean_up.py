# Load Modules
import pandas as pd
import spacy
import string

# Load Pre-Trained Language Model from spaCy
nlp = spacy.load('en_core_web_md')

# Load title collection of Reddit
df = pd.read_csv('../0_DATA/raw/reddit_titles_uncleaned.csv')

# --- Clean-Up : Remove special Characters
punctuation = string.punctuation
punctuation = punctuation.replace('.', '')
punctuation = punctuation.replace("\'", "")
punctuation = punctuation.replace('\"', '')
punctuation = punctuation.replace(',', '')
punctuation = punctuation.replace('!', '')
punctuation = punctuation.replace('?', '')

df = df.apply(lambda x: x.translate(str.maketrans('', '', punctuation)))

# Initiate the Doc-Objects
df = df.apply(lambda x: nlp(x))

# --- Clean-Up : Remove paths / urls
df = df.apply(lambda x: [token for token in x if not token.like_url])


# --- Clean-Up : Remove emails
df = df.apply(lambda x: [token for token in x if not token.like_email])


# --- Clean-Up : Remove Interjectons
def remove_interjection(x):
    return [token for token in x if token.pos_ != 'INTJ']

df = df.apply(remove_interjection)


# --- Clean-Up : Remove Numbers
df = df.apply(lambda x: [token for token in x if not token.like_num])


# write to csv
df = df.apply(lambda x: " ".join([token.text for token in x]))
df.to_csv('../0_DATA/raw/reddit_titles_cleaned.csv')