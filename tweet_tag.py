import pandas as pd
import os
from reader import ReadFile
import pickle
START_FROM_BACKUP = False


def read_querys_from_txt(querys_path):
    with open(querys_path, encoding='utf-8') as f:
        content = f.readlines()
    queries = [x.strip() for x in content if x != '\n']
    return queries

querys_path = "C:\\Users\\eilam gal\\Search_Engine\\part_two\\full_queries.txt"
tweet_to_annotate_path = "C:\\Users\\eilam gal\\Search_Engine\\part_two\\305786451.csv"
data_path = "C:\\Users\\eilam gal\\Search_Engine\\part_two\\Data"
output_path = os.path.join(os.path.dirname(__file__), 'annotation.csv')
queries = read_querys_from_txt(querys_path)
tweets_queries_df = pd.read_csv(tweet_to_annotate_path)
tweets_queries_dict = tweets_queries_df.set_index('tweet').T.to_dict('records')[0]
tweets_queries_df.set_index('tweet', inplace=True)
rdr = ReadFile(data_path)
tweet_annotation_dict = {}
start_from_backup = START_FROM_BACKUP
tweet_num = 1
last_tweet_num = 0
if start_from_backup:
    with open("backup_file.pkl", 'rb') as f:
        ls = pickle.load(f)
        tweet_annotation_dict = f[0]
        last_tweet_num = [1]
for dir in os.listdir(data_path):
    dir_path = os.path.join(data_path, dir)
    if not os.path.isdir(dir_path):
        continue
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir, file)
        if file[-7:] != "parquet":
            continue
        print(f'Reading {file}...')
        file_as_list = rdr.read_file(file_path)
        for tweet in file_as_list:
            if int(tweet[0]) in tweets_queries_dict:
                if start_from_backup:
                    tweet_num += 1
                    if tweet_num == last_tweet_num:
                        start_from_backup = False
                    break
                print(f"Query: {queries[tweets_queries_dict[int(tweet[0])]-1]}")
                print(f"Tweet {tweet_num}/{len(tweets_queries_dict)}:\n{tweet}")
                annotation = ""
                while annotation != 0 and annotation !=1:
                    try:
                        annotation = int(input("is the tweet relevant for the query (1:yes,0:no)? "))
                    except:
                        print("please enter a valid number")
                tweet_annotation_dict[int(tweet[0])] = annotation
                tweet_num += 1
                if not start_from_backup and tweet_num % 10 == 0:
                    with open("backup_file.pkl", 'wb') as f:
                        backup = []
                        backup.append(tweet_annotation_dict)
                        backup.append(tweet_num)
                        pickle.dump(backup, f)
                print("\n")


tweet_annotation_df = pd.DataFrame.from_dict(tweet_annotation_dict.items())
tweet_annotation_df.rename(columns={0: "tweet", 1: "label"}, inplace=True)
tweet_annotation_df.set_index('tweet', inplace=True)
output = tweets_queries_df.merge(tweet_annotation_df, left_on='tweet', right_on='tweet')
output.to_csv(output_path)