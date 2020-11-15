class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # Update inverted index and posting
                if term.lower not in self.inverted_idx.keys() and term.upper() not in self.inverted_idx.keys():
                    self.inverted_idx[term] = 1
                    self.postingDict[term] = []

                elif term.isupper() and term.lower in self.inverted_idx.keys():
                    self.inverted_idx[term.lower] += 1
                    term = term.lower()

                elif term.islower() and term.upper in self.inverted_idx.keys():
                    self.inverted_idx[term] = self.inverted_idx[term.upper] + 1
                    del self.inverted_idx[term.upper]
                    self.postingDict[term] = self.postingDict[term.upper]
                    del self.postingDict[term.upper]

                else:
                    self.inverted_idx[term] += 1

                self.postingDict[term].append((document.tweet_id, document_dictionary[term]))

            except:
                print('problem with the following key {}'.format(term[0]))

