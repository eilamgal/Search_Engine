import time

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils


def run_engine():
    """

    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)

    documents_list = r.read_file(file_name='sample4.parquet')
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
        indexer.add_new_doc(parsed_document)
     #   print('Finished indexing document after {0} seconds.'.format(time.time() - start_time))
    #    print()
    print('Finished parsing and indexing after {0} seconds. Starting to export files'
          .format(time.time()-global_start_time))
    indexer.finish_indexing()
    print(indexer.inverted_idx)
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
