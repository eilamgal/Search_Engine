from postings_handler import PostingsHandler
import utils
import numpy


class Indexer:
    def __init__(self, config):
        self.config = config
        self.inverted_idx = {}
        #self.entities_inverted_idx = {term0 : [idf(term0), address of term0 on the disk = (posting file num,position in this posting file)], term1 : ...}
        self.entities_inverted_idx = {}
        #self.entities_postingDict = []
        self.entities_posting_handler = PostingsHandler(config, number_of_buckets=2, first_bucket_index=80)
        self.posting_handler = PostingsHandler(config, 10)
        self.document_dict = {} # {doc0_id:[0-date, 1-corpus_referrals, 2-unique_words, 3-max_tf(doc0), 4-tweet length, tweet glove vector] ,...}
        self.referrals_counter = {}
        self.debug_tweet_counter = 0
        self.avg_tweet_length = 0

    def add_new_doc(self, document, golve_dict=None):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        entities_doc_dictionary = document.entities_doc_dictionary
        if entities_doc_dictionary:
            for entity in entities_doc_dictionary.keys():
                if entity not in self.entities_inverted_idx.keys():
                    self.entities_inverted_idx[entity] = [1, (-1, -1)]
                else:
                    self.entities_inverted_idx[entity][0] += 1
                self.entities_posting_handler.append_term(entity, document.tweet_id, entities_doc_dictionary[entity],
                                                          self.entities_inverted_idx)
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        self.document_dict[document.tweet_id] = [document.tweet_date, 0, len(document_dictionary.keys()) +
                                                 len(entities_doc_dictionary.keys()), -1, 0, document.tweet_length]
        self.avg_tweet_length += (1/10000000)*document.doc_length
        tweet_vector = numpy.full(25, 0)
        for term in document_dictionary.keys():
            #try:
                # Update inverted index and posting
                frequency = document_dictionary[term]
                if term in golve_dict.keys():
                    tweet_vector = tweet_vector + (frequency/document.tweet_length)*golve_dict[term]
                if term.lower() not in self.inverted_idx.keys() and term.upper() not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [1, (-1, -1)]
                elif term.isupper() and term.lower() in self.inverted_idx.keys():
                    self.inverted_idx[term.lower()][0] += 1
                    term = term.lower()
                elif term.islower() and term.upper() in self.inverted_idx.keys():
                    self.inverted_idx[term] = [self.inverted_idx[term.upper()][0] + 1,
                                               self.inverted_idx[term.upper()][1]]
                    del self.inverted_idx[term.upper()]
                    self.posting_handler.change_term_case(term.upper(), term)
                else:
                    self.inverted_idx[term][0] += 1
                self.posting_handler.append_term(term, document.tweet_id, frequency, self.inverted_idx)
            #except:
                #print('problem with the following key {}'.format(term) + " ID = " + document.tweet_id)
        self.document_dict[document.tweet_id].append(tweet_vector)
        if document.referrals_ids:
            for referral in document.referrals_ids:
                if referral not in self.referrals_counter.keys():
                    self.referrals_counter[referral] = 1
                else:
                    self.referrals_counter[referral] += 1
        self.debug_tweet_counter += 1
        if self.debug_tweet_counter % 1000000 == 0:
            print(self.debug_tweet_counter)

    def finish_indexing(self):
        self.posting_handler.finish_indexing(self.inverted_idx)

        self.__check_entities()
        #utils.save_obj(self.entities_postingDict, "bucket"+str(80))
        self.inverted_idx.update(self.entities_inverted_idx)
        self.__update_referrals()
        utils.save_obj(self.document_dict, "docDictionary")

    def __check_entities(self):
        for entity in self.entities_inverted_idx.keys():
            if self.entities_inverted_idx[entity][0] > 1:
                self.inverted_idx[entity] = self.entities_inverted_idx[entity]
        self.entities_posting_handler.finish_indexing(self.entities_inverted_idx)
        self.entities_inverted_idx.clear()

    def __update_referrals(self):
        for doc_id in self.document_dict.keys():
            if doc_id in self.referrals_counter.keys():
                self.document_dict[doc_id][1] = self.referrals_counter[doc_id]


