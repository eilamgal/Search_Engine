from postings_handler import PostingsHandler


class Indexer:
    def __init__(self, config):
        self.config = config
        self.inverted_idx = {}
        #self.postingDict = {}
        self.entities_inverted_idx = {}
        self.entities_postingDict = {}
        self.posting_handler = PostingsHandler(config)

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        """
        entities_doc_dictionary = document.entities_doc_dictionary
        if entities_doc_dictionary:
            for entity in entities_doc_dictionary.keys():
                if entity not in self.entities_inverted_idx.keys():
                    self.entities_inverted_idx[entity] = [1, -1]
                    self.entities_postingDict[entity] = []
                else:
                    self.entities[entity][0] += 1
                self.entities_postingDict[entity].append(document.tweet_id, entities_doc_dictionary[entity])
        """
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc

        # if document.tweet_id == "1281197184482832384":
        #     print()
        for term in document_dictionary.keys():
            #try:
                # Update inverted index and posting
                frequency = document_dictionary[term]
                if term.lower() not in self.inverted_idx.keys() and term.upper() not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [1, -1]
                    #self.postingDict[term] = []

                elif term.isupper() and term.lower() in self.inverted_idx.keys():
                    self.inverted_idx[term.lower()][0] += 1
                    term = term.lower()

                elif term.islower() and term.upper() in self.inverted_idx.keys():
                    self.inverted_idx[term] = [self.inverted_idx[term.upper()][0] + 1,
                                               self.inverted_idx[term.upper()][1]]
                    #self.inverted_idx[term][0] = self.inverted_idx[term.upper()][0] + 1
                    del self.inverted_idx[term.upper()]
                    self.posting_handler.change_term_case(term.upper(), term)
                    #self.postingDict[term] = self.postingDict[term.upper()]
                    #del self.postingDict[term.upper()]

                else:
                    self.inverted_idx[term][0] += 1

                self.posting_handler.append_term(term, document.tweet_id, frequency, self.inverted_idx)
                #self.postingDict[term].append((document.tweet_id, frequency))

            #except:
                #print('problem with the following key {}'.format(term) + " ID = " + document.tweet_id)

    def finish_indexing(self):
        self.posting_handler.finish_indexing(self.inverted_idx)

    def __check_entities(self):
        for entity in self.entities_inverted_idx.keys():
            if self.entities_inverted_idx[entity] < 2:
                del self.entities_postingDict[entity]
                del self.entities_inverted_idx[entity]
