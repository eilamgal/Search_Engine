from bucket import Bucket
import utils
import time
MAX_SIZE = 1000000


class TweetVectorsHandler:
    """
    Similar to the postings_handler, but simpler - builds a dictionary for tweets and their average Glove vectors
    and dumps them to the disk once MAX_SIZE is reached in memory.
    """
    def __init__(self, config, first_bucket_index=0):
        self.bucket = Bucket()
        self.bucket_index = first_bucket_index
        self.size = 0
        self.config = config

    def __flush_bucket(self, doc_dictionary):  # just write to the desk and clean the bucket
        new_posting = []
        for term in self.bucket.get_dict_terms():
            new_posting.append(self.bucket.get_term_posting(term)[0])
            doc_dictionary[term][5] = (self.bucket_index, len(new_posting) - 1)

        self.size = 0
        self.bucket.clean_bucket()
        start_time = time.time()
        utils.save_obj(new_posting, "avgVector" + str(self.bucket_index))
        # print("glove vector write time: ", time.time()-start_time)
        self.bucket_index += 1

    def append_tweet(self, doc_id, vector, inverted_idx):  # gets tweet vector for insert to the bucket
        self.bucket.append_tweet(doc_id, vector)
        self.size += 1
        if self.size > MAX_SIZE:
            self.__flush_bucket(inverted_idx)

    def finish_indexing(self, doc_dictionary):
        self.__flush_bucket(doc_dictionary)

