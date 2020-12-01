from parser_module import Parse
from ranker import Ranker
import utils
import math
from numpy import dot
from numpy.linalg import norm
import numpy as np

def bm25(corpus_term_frequency, tweet_term_frequency, avg_tweet_length, tweet_length, corpus_size=10000000, k=1.4,
         b=0.75, base=10):
    return ((tweet_term_frequency * (1 + k)) / (
                tweet_term_frequency + k * (1 - b + b * (tweet_length / avg_tweet_length)))) * math.log(
        (corpus_size + 1) / corpus_term_frequency, base)


def cosine(vector1, vector2):
    return dot(vector1, vector2)/((norm(vector1))*(norm(vector2)))


def euclidean_distance(vector1, vector2):
    return np.norn(vector1, vector2)


class Searcher:

    def __init__(self, inverted_index, tweet_dict, avg_tweet_length):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.tweet_dict = tweet_dict###
        self.avg_tweet_length = avg_tweet_length###

    def relevant_docs_from_posting(self, query, glove_dict=None):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        query_vector = np.full(25, 0)
        for term in query:
            if term.lower() in glove_dict.keys():
                query_vector = query_vector + (1/len(query))*glove_dict[term.lower()]
            elif term.upper() in glove_dict.keys():
                query_vector = query_vector + (1 / len(query)) * glove_dict[term.upper()]
            elif term in glove_dict.keys():
                query_vector = query_vector + (1 / len(query)) * glove_dict[term.lower]
        #posting = utils.load_obj("posting")
        relevant_docs = {} #{doc ID : [0-golve score(some agabric distance), 1-BM25, 2-retweet score, 3-time score(more update better score)]}
        for term in query:
            try: # an example of checks that you have to do
                if term not in self.inverted_index.keys():
                    if term.islower() and term.upper() in self.inverted_index.keys():
                        term = term.upper()
                    elif term.isupper() and term.lower() in self.inverted_index.keys():
                        term = term.lower()
                    else:
                        continue
                posting = utils.load_obj("bucket"+str(self.inverted_index[term][1][0]))
                #posting_doc = posting[term]
                posting_doc = posting[self.inverted_index[term][1][1]]
                for doc_tuple in posting_doc:
                    doc = doc_tuple[0]
                    if doc not in relevant_docs.keys():
                        relevant_docs[doc] = [cosine(query_vector, self.tweet_dict[doc][6]), bm25(self.inverted_index[term][0],
                                                                                              doc_tuple[1], self.avg_tweet_length, self.tweet_dict[doc][4]),
                                              self.tweet_dict[doc][1], self.tweet_dict[doc][0]]
                    else:
                        relevant_docs[doc][1] += bm25(self.inverted_index[term][0], doc_tuple[1], self.avg_tweet_length,
                                                      self.tweet_dic[doc_tuple[0]][4])
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs




