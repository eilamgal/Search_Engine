from bucket import Bucket
import utils
MAX_SIZE = 1000000


class TweetPostingHandler:
    def __init__(self, config, number_of_buckets=6, first_bucket_index=0):
        self.bucket = Bucket()
        self.bucket_index = first_bucket_index
        self.size = 0
        self.config = config

    def __flush_bucket(self, inverted_idx):
        new_posting = []
        for term in self.bucket.get_dict_terms():
            new_posting.append([])
            inverted_idx[term][6] = (self.bucket_index, len(new_posting) - 1)
            new_posting[inverted_idx[term][6][1]].extend(self.bucket.get_term_posting(term))
        self.size = 0
        self.bucket.clean_bucket()
        utils.save_obj(new_posting, "bucket" + str(self.bucket_index))
        self.bucket_index += 1

    def append_term(self, doc_id, vector, inverted_idx):
        self.bucket.append_tweet(doc_id, vector)
        self.size += 1
        if self.size > MAX_SIZE:
            self.__flush_bucket(inverted_idx)

    def finish_indexing(self, inverted_idx):
        self.__flush_bucket(inverted_idx)

