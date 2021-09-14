# Load Modules
from modules.api import API
import pandas as pd
import time


def submissions():
    unfiltered_df = get_submissions("techsupport", 2000)
    filtered_df = filter_submissions(unfiltered_df)
    filtered_df.to_csv('../0_DATA/reddit_titles_uncleaned.csv')
    print("FINISH", filtered_df.shape)

def get_submissions(subreddit, days):
    epoch_time = int(time.time())
    results = []

    submission = API("https://api.pushshift.io/reddit/search/submission/")
    for index in range(days*8):
        submission.add_query(subreddit=subreddit, before=f"{epoch_time-(index*10800)}", after=f"{epoch_time-((1+index)*10800)}", sort='desc', sort_type='score')
        response = submission.request()
        if response != None:
            results.append(pd.DataFrame(response["data"]))
        time.sleep(1)

    df = pd.concat(results, ignore_index=True).drop_duplicates(subset='id').reset_index(drop=True)
    return df

def filter_submissions(df: pd.DataFrame) -> pd.DataFrame:
    result = df[(df['is_self'] == True) & (df['score'] >= 3)]
    subset = ['title']
    result = result[subset]
    return result
    