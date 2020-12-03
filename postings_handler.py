from bucket import Bucket
import pickle
import utils
import os
MAX_SIZE = 1000000
THRESHOLD = 200000
BUCKET_ID = 0
abc_frequency_dict = {'a': 1.7, 'b': 4.4, 'c': 5.2, 'd': 3.2, 'e': 2.8, 'f': 4, 'g': 1.6, 'h': 4.2, 'i': 7.3, 'j': 7.3,
                      'k': 0.86, 'l': 2.4, 'm': 3.8, 'n': 2.3, 'o': 7.6, 'p': 4.3, 'q': 0.22, 'r': 2.8, 's': 6.7,
                      't': 16, 'u': 1.2, 'v': 0.82, 'w': 5.5, 'x': 0.045, 'y': 0.76, 'z': 0.045}

"""
def initialize_buckets(num_of_buckets, first_bucket_index=0):
    for i in range(num_of_buckets):
        utils.save_obj([], "bucket" + str(i))
"""


def get_bucket_index_by_term(term, number_of_bukcets):
    if len(term) == 0 or not term[0].isalpha():
        if len(term) > 1 and term[1].isalpha():
            return (ord(term[1].lower())-ord('a')) % number_of_bukcets
        else:
            return number_of_bukcets-1
    else:
        return (ord(term[0].lower()) - ord('a')) % number_of_bukcets


class PostingsHandler:
    def __init__(self, config, number_of_buckets=6, first_bucket_index=0, contains="terms"):

        if contains == "terms":
            number_of_buckets = config.get_number_of_term_buckets()
        elif contains == "entities":
            number_of_buckets = config.get_number_of_entities_buckets()
            first_bucket_index = config.get_entities_index()

        self.buckets = []
        self.terms_dict = {}
        self.size = 0
        # self.config = config
        self.__equal_width_buckets(number_of_buckets)
        self.buckets_mapping = {}
        self.initialize_buckets(number_of_buckets, first_bucket_index)

    def initialize_buckets(self, num_of_buckets, first_bucket_index=0):
        for i in range(num_of_buckets):
            utils.save_obj([], "bucket" + str(first_bucket_index + i))
            self.buckets_mapping[i] = first_bucket_index + i

    def __flush_bucket(self, inverted_idx, bucket_index):
        # print("disk operation")
        new_posting = utils.load_obj("bucket" + str(self.buckets_mapping[bucket_index]))
        for term in self.buckets[bucket_index].get_dict_terms():
            if inverted_idx[term][1][1] < 0:
                new_posting.append([])
                inverted_idx[term][1] = (self.buckets_mapping[bucket_index], len(new_posting) - 1)
            new_posting[inverted_idx[term][1][1]].extend(self.buckets[bucket_index].get_term_posting(term))
        self.size -= self.buckets[bucket_index].get_size()
        self.buckets[bucket_index].clean_bucket()
        utils.save_obj(new_posting, "bucket" + str(self.buckets_mapping[bucket_index]))

    def __equal_width_buckets(self, number_of_buckets):
        for key in abc_frequency_dict.keys():
            self.terms_dict[key] = (ord(key)-ord('a')) % number_of_buckets
        for i in range(number_of_buckets):
            new_bucket = Bucket()
            self.buckets.append(new_bucket)

    def __find_the_biggest_bucket(self):
        max_size_bucket = 0
        for i in range(1, len(self.buckets)):
            if max_size_bucket < self.buckets[i].get_size():
                max_size_bucket = i
        return max_size_bucket

    def append_term(self, term, doc_id, frequency, inverted_idx):
        if len(term) == 0 or not term[0].isalpha():
            if len(term) > 1 and term[1].isalpha():
                self.buckets[self.terms_dict[term[1].lower()]].append_term(term, doc_id, frequency)
            else:
                self.buckets[-1].append_term(term, doc_id, frequency)
        else:
            self.buckets[self.terms_dict[term[0].lower()]].append_term(term, doc_id, frequency)
        self.size += 1
        if self.size > MAX_SIZE:
            for i in range(len(self.buckets)):
                if self.buckets[i].get_size() > THRESHOLD:
                    self.__flush_bucket(inverted_idx, i)

    def change_term_case(self, old_term, new_term):
        self.buckets[self.terms_dict[old_term[0].lower()]].rename_key(old_term, new_term)

    def finish_indexing(self, inverted_idx):
        for i in range(len(self.buckets)):
            if self.buckets[i].get_size != 0:
                self.__flush_bucket(inverted_idx, i)


