import bucket
MAX_SIZE = 566
terms_dict = {}

def flush_bucket():




class postings_handler:
    def __init__(self, config, number_of_buckets=6):
            self.buckets = []
            self.terms_dict = {}
            self.size = 0
            self.config = config

    def append_term(self, term, doc_id, frequency):
            self.buckets[terms_dict[term[0]]].append(term,doc_id,frequency)
            bucket_t = bucket()


