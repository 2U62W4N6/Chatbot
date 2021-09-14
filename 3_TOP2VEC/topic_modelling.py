# Load Modules
from top2vec import Top2Vec
import pandas as pd

# Load title collection of Reddit
df = pd.read_csv('../0_DATA/raw/reddit_titles_top2vec.csv')
titles = df.values.tolist()


# Initiate Top2Vec Model with pre-trained language model
model = Top2Vec(titles, speed='deep-learn', embedding_model='universal-sentence-encoder')


# Retrieve the top 10 topics based on the size and generate wordclouds
topic_nums = model.get_topics(10)
for topic in topic_nums:
    model.generate_topic_wordcloud(topic) 


# Append to each data point the corespodning topic that it was clustered
results = []
for topic in topic_nums:
    documents = model.search_documents_by_topic(topic_num=topic, num_docs=500)
    df = pd.DataFrame(documents, columns =['titles'])
    df['topic'] = topic
    results.append(df)

df = pd.concat(results, ignore_index=True).drop_duplicates(subset='id').reset_index(drop=True)


# write to csv
df = pd.to_csv('../0_DATA/raw/reddit_titles_labeled.csv')