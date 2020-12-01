import time
import sys
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
from glove import GloveStrategy
import os
import glob
import regex as re

def run_engine():
    """

    :return:
    """
    number_of_documents = 0

    # config = ConfigClass("C:\\Users\\odedber\\PycharmProjects\\Search_Engine")
    # glove_dict = GloveStrategy(
    #     "C:\\Users\\odedber\\PycharmProjects\\Search_Engine\\glove.twitter.27B.25d.txt").embeddings_dict

    config = ConfigClass("C:\\Users\\eilam gal\\Search_Engine")
    glove_dict = GloveStrategy(
        "C:\\Users\\eilam gal\\Desktop\\סמסטר\\סמסטר ז\\IR\\glove.twitter.27B.25d.txt").embeddings_dict
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
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

    documents_list = [path for path in r.read_file(file_name='sample4.parquet')]
    glove_dict = GloveStrategy("C:\\Users\\eilam gal\\Desktop\\סמסטר\\סמסטר ז\\IR\\glove.twitter.27B.25d.txt").embeddings_dict
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
   # print(indexer.inverted_idx)
    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    #utils.save_obj(indexer.postingDict, "posting")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    p = Parse()
    #
    #query_as_list = p.parse_sentence(query)
    query_as_list, x = p.parse_text(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main():
    run_engine()
    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
