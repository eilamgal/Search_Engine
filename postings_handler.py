from bucket import Bucket
import pickle
import utils
import os
MAX_SIZE = 1000000
THRESHOLD = 200000
abc_frequency_dict = {'a': 1.7, 'b': 4.4, 'c': 5.2, 'd': 3.2, 'e': 2.8, 'f': 4, 'g': 1.6, 'h': 4.2, 'i': 7.3, 'j': 7.3, 'k': 0.86, 'l': 2.4, 'm': 3.8, 'n': 2.3, 'o': 7.6, 'p': 4.3, 'q': 0.22, 'r': 2.8, 's': 6.7, 't': 16, 'u': 1.2, 'v': 0.82, 'w': 5.5, 'x': 0.045, 'y': 0.76, 'z': 0.045}


def initialize_buckets(num_of_buckets):
    for i in range(num_of_buckets):
        utils.save_obj([], "bucket" + str(i))
        """
        try:
            outfile = open(self.config.get_saveFilesWithStem()+"bucket" + str(i) + '.pkl', "wb")
            pickle.dump([], outfile)
            outfile.close()
        except:
            print('problem with open file posting{}.pkl'.format(i))
        """
class PostingsHandler:
    def __init__(self, config, number_of_buckets=6):
        self.buckets = []
        self.terms_dict = {}
        self.size = 0
        self.config = config
        self.__equal_width_buckets(number_of_buckets)
        initialize_buckets(number_of_buckets)

    def __flush_bucket(self, inverted_idx, bucket_index):
        """
        try:
            infile = open(self.config.get_saveFilesWithStem()+"\\bucket" + str(bucket_index) + '.pkl', "wb")
            new_posting = pickle.load(infile)
            infile.close()
        except:
            print('problem with open file posting{}.pkl'.format(bucket_index))

        print("disk operation")
        """
        print("disk operation")
        new_posting = utils.load_obj("bucket" + str(bucket_index))
        for term in self.buckets[bucket_index].get_dict_terms():
            if inverted_idx[term][1][1] < 0:
                new_posting.append([])
                inverted_idx[term][1] = (bucket_index, len(new_posting) - 1)
            new_posting[inverted_idx[term][1][1]].extend(self.buckets[bucket_index].get_term_posting(term))
        self.size -= self.buckets[bucket_index].get_size()
        self.buckets[bucket_index].clean_bucket()
        utils.save_obj(new_posting, "bucket" + str(bucket_index))
        """
       try:
           outfile = open(self.config.get_saveFilesWithStem()+"\\bucket" + str(bucket_index), "wb")
           pickle.dump(new_posting, outfile)
           outfile.close()
       except:
           print('problem with open file posting{}.pkl'.format(bucket_index))
       """

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
            self.buckets[len(self.buckets)-1].append_term(term, doc_id, frequency)
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


