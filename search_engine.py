import time
import sys
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
from glove import GloveStrategy
import glob


def run_engine(corpus_path="testData", output_path="posting", stemming=True):
    """
    This function build the inverted index over the corpus.
    send each tweet to parsing and indexing.
    if the steming is True so the parsing will use stammer on the tokens.
    :param corpus_path
    :param output_path for the inverted index
    :param stemming if True so use stammer on terms
    """
    glove_dict = GloveStrategy("glove.twitter.27B.25d.txt").embeddings_dict
    #glove_dict = GloveStrategy("../../../../glove.twitter.27B.25d.txt").embeddings_dict  # Web system
    config = ConfigClass(corpus_path, number_of_term_buckets=26, number_of_entities_buckets=2)
    r = ReadFile(corpus_path=config.get_corpusPath())
    p = Parse(stemming)
    indexer = Indexer(config)
    all_files_paths = glob.glob(config.get_corpusPath() + "\\*\\*.snappy.parquet")
    all_files_names = [file_name[file_name.find("\\") + 1:] for file_name in all_files_paths]
    start_time = time.time()
    file_counter = 0
    for file_name in all_files_names:
        file_start_time = time.time()
        print("start file :", file_counter)
        documents_list = [document for document in r.read_file(file_name=file_name)]
        # Iterate over every document in the file
        for idx, document in enumerate(documents_list):
            parsed_document = p.parse_doc(document)
            indexer.add_new_doc(parsed_document, glove_dict)
        print("end file number ", file_counter, " in: ", time.time() - file_start_time)
        file_counter += 1
    total_time = time.time() - start_time
    indexer.finish_indexing()
    print('Finished parsing and indexing after {0} seconds. Starting to export files'.format(total_time))


def load_index():
    # print('Load inverted index')
    inverted_index = utils.load_obj("inverted_index")
    return inverted_index


def load_tweet_dict():  # read all the tweet vector files and insert the vectors to the tweet dictionary
    tweet_dict = utils.load_obj("docDictionary")
    buckets = []
    for i in range(tweet_dict["metadata"]["tweet_vector_buckets"]):
        buckets.append(utils.load_obj("avgVector" + str(i)))
    for tweet_id in tweet_dict.keys():
        if tweet_id == "metadata":
            continue
        address = tweet_dict[tweet_id][5]
        tweet_dict[tweet_id][5] = buckets[address[0]][address[1]]
    return tweet_dict


def search_and_rank_query(query, inverted_index, k, glove_dict="", tweet_dict=None):
    """
    This function gets query and return top k tweet that is relevant for the query.
    first parse the query and then search all relevant tweets for the query in the inverted index
    """
    p = Parse()
    query_as_list, entities = p.parse_text(query)
    full_query = query_as_list + entities
    searcher = Searcher(inverted_index, tweet_dict)
    relevant_docs = searcher.relevant_docs_from_posting(full_query, glove_dict=glove_dict)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    retrive_list = searcher.ranker.retrieve_top_k(ranked_docs, k)
    return retrive_list


def main(corpus_path="testData", output_path="posting", stemming=False, queries='', num_docs_to_retrieve=10):
    # run_engine()
    run_engine(corpus_path=corpus_path, output_path=output_path, stemming=stemming)

    # start = time.time()
    # tweet_dict = load_tweet_dict()
    # print(time.time()-start)
    #
    # glove_dict = GloveStrategy(
    #     "C:\\Users\\odedber\\PycharmProjects\\Search_Engine\\glove.twitter.27B.25d.txt").embeddings_dict
    # query = input("Please enter a query: ")
    # k = int(input("Please enter number of docs to retrieve: "))
    # inverted_index = load_index()
    # results = search_and_rank_query(query, inverted_index, k, glove_dict, tweet_dict)
    # for doc_tuple in results:
    #     print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
