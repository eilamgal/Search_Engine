import time
from glove import GloveStrategy
from reader import ReadFile
import search_engine
import csv



GLOVE_WEIGHT = 0.3
BM25_WEIGHT = 0.2
REFERRAL_WEIGHT = 0.3
RELEVANCE_WEIGHT = 0.3


if __name__ == '__main__':
    inverted_index = search_engine.load_index()
    tweet_dict = search_engine.load_tweet_dict()
    reader = ReadFile(corpus_path="testData")
    queries = reader.load_queries("queries.txt")
    print()
    glove_dict = GloveStrategy("glove.twitter.27B.25d.txt").embeddings_dict
    start = time.time()

    results_file = open('results.csv', mode='w', newline='')
    results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for idx, query in enumerate(queries):
        results = search_engine.search_and_rank_query(query, inverted_index, 5, glove_dict, tweet_dict)
        for result in results:
            result[1].append(GLOVE_WEIGHT*result[1][0]
                             + BM25_WEIGHT*result[1][1]
                             + REFERRAL_WEIGHT*result[1][2]
                             + RELEVANCE_WEIGHT*result[1][3])
            print(idx+1, result[0], result[1][4])
            results_writer.writerow([idx+1, result[0], result[1][4]])
    print("Finished after : {0} seconds".format(time.time()-start))
    results_file.close()
