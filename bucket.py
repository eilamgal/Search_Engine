class Bucket:
    def __init__(self):
        self.dict = {}
        self.size = 0

    def append_term(self, term, doc_id, frequency):
        if term not in self.dict.keys():
            self.dict[term] = []
        self.dict[term].append((doc_id, frequency))
        self.size += 1

    def append_tweet(self, doc_id, vector):
        if doc_id not in self.dict.keys():
            self.dict[doc_id] = []
        self.dict[doc_id].append(vector)
        self.size += 1

    def get_size(self):
        return self.size

    def clean_bucket(self):
        self.dict.clear()
        self.size = 0

    def get_term_posting(self, term):
        if term in self.dict.keys():
            return self.dict[term]

    def get_dict_terms(self):
        return self.dict.keys()

    def rename_key(self, old_term, new_terms):
        if old_term in self.dict.keys():
            self.dict[new_terms] = self.dict[old_term]
            del self.dict[old_term]
