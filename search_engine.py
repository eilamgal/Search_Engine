import time
import sys
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
from glove import GloveStrategy


def run_engine(corpus_path="", output_path="", stemming=False):
    """
    :return:
    """
    number_of_documents = 0
    config = ConfigClass(corpus_path)
    # glove_dict = GloveStrategy(
    #     "C:\\Users\\odedber\\PycharmProjects\\Search_Engine\\glove.twitter.27B.25d.txt").embeddings_dict

    # config = ConfigClass("C:\\Users\\eilam gal\\Search_Engine")
    glove_dict = GloveStrategy(
        "C:\\Users\\eilam gal\\Desktop\\סמסטר\\סמסטר ז\\IR\\glove.twitter.27B.25d.txt").embeddings_dict

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(stemming)
    indexer = Indexer(config)
    """
    all_files_paths = glob.glob(config.get__corpusPath()+"\\*\\*.snappy.parquet")
    all_files_names = [file_name[-44:] for file_name in all_files_paths]
    for file_path in all_files_names:
        print(file_path)
        documents_list = [path for path in r.read_file(file_name=file_path)]
        global_start_time = time.time()
        # Iterate over every document in the file
        for idx, document in enumerate(documents_list):
            # parse the document
            # start_time = time.time()
            if len(indexer.inverted_idx.keys()) % 10000 == 0:
                print(len(indexer.inverted_idx.keys()))
            parsed_document = p.parse_doc(document)
            #  print('Finished parsing document after {0} seconds.'.format(time.time() - start_time))
            # start_time = time.time()
            number_of_documents += 1
            # index the document data
            indexer.add_new_doc(parsed_document, glove_dict)
    """
    #all_files_paths = glob.glob(config.get__corpusPath()+"\\*\\*.snappy.parquet")

    documents_list = [path for path in r.read_file(file_name='date=07-08-2020/covid19_07-08.snappy.parquet')]
    # glove_dict = GloveStrategy("C:\\Users\\odedber\\PycharmProjects\\Search_Engine\\glove.twitter.27B.25d.txt").embeddings_dict
    global_start_time = time.time()
    # Iterate over every document in the file
    for idx, document in enumerate(documents_list):
        # parse the document
       # start_time = time.time()
        if len(indexer.inverted_idx.keys()) % 10000 == 0:
            print(len(indexer.inverted_idx.keys()))
        parsed_document = p.parse_doc(document)
      #  print('Finished parsing document after {0} seconds.'.format(time.time() - start_time))
        #start_time = time.time()
        number_of_documents += 1
        # index the document data
        indexer.add_new_doc(parsed_document, glove_dict)
     #   print('Finished indexing document after {0} seconds.'.format(time.time() - start_time))
    #    print()
    print('Finished parsing and indexing after {0} seconds. Starting to export files'
          .format(time.time()-global_start_time))
    print(len(indexer.inverted_idx.keys()))
    print(len(indexer.entities_inverted_idx.keys()))
    print("indexer.inverted_idx size: " + str(sys.getsizeof(indexer.inverted_idx)))
    print("indexer.entities_inverted_idx size: " + str(sys.getsizeof(indexer.entities_inverted_idx)))
#    print("indexer.entities_postingDict size: " + str(sys.getsizeof(indexer.entities_postingDict)))
   # """
    indexer.finish_indexing()
    #avg_tweet_length = indexer.avg_tweet_length
    utils.save_obj(indexer.inverted_idx, "inverted_idx")

    #utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def load_tweet_dict():
    tweet_dict = utils.load_obj("docDictionary")
    buckets = []
    for i in range(tweet_dict["tweet_vector_buckets"]):
        buckets.append(utils.load_obj("bucket"+str((40+i))))
    for tweet_id in tweet_dict.keys():
        address = tweet_dict[tweet_id][5]
        tweet_dict[tweet_id][5] = buckets[address[0]][address[1]]
    return tweet_dict


def search_and_rank_query(query, inverted_index, k, glove_dict="", tweet_dict=None):
    p = Parse()
    start_time = time.time()
    query_as_list, entities = p.parse_text(query)
    full_query = query_as_list + entities
    searcher = Searcher(inverted_index, tweet_dict)
    relevant_docs = searcher.relevant_docs_from_posting(full_query, glove_dict=glove_dict)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    print("IR time: ", time.time()-start_time)
    start_time = time.time()
    retrive_list = searcher.ranker.retrieve_top_k(ranked_docs, k)
    print("time to retrieve_top_k: ", time.time()-start_time)
    return retrive_list


def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    run_engine(corpus_path, output_path, stemming)

    # tweet_dict = load_tweet_dict()
    # glove_dict = GloveStrategy(
    #     "C:\\Users\\odedber\\PycharmProjects\\Search_Engine\\glove.twitter.27B.25d.txt").embeddings_dict
    #
    # query = input("Please enter a query: ")
    # k = int(input("Please enter number of docs to retrieve: "))
    # inverted_index = load_index()
    # results = search_and_rank_query(query, inverted_index, k, glove_dict, tweet_dict)
    # for doc_tuple in results:
    #     print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
