from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document


def remove_urls(full_text):
    if not full_text:
        return
    split = full_text.split(' ')
    clean = [token for token in split if "http" not in token.lower()]
    # for token in split:
    #     if "http" not in token.lower():
    #         clean.append(token)
    return ' '.join(clean)


def expand_url(url):
    if not url:
        return
    url_split = url.find("\":\"")
    long_url = url[url_split + 3:]
    return long_url[:len(long_url) - 2]


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords

    # def handle_urls(self, doc):
    #     """
    #     This function processes a doc_list, replaces shortened urls with full ones and tokenize them
    #     :param doc: raw doc_list from file reader
    #     :return: clean doc_list without unhandled URLs
    #     """
    #     full_text = doc[2].split(' ')
    #     url = doc[3]
    #     url_indices = doc[4]
    #     quote_text = []
    #     quote_url = {}
    #     quote_url_indices = []
    #     if doc[8]:
    #         quote_text = doc[8].split(' ')
    #         quote_url = doc[9]
    #         quote_url_indices = doc[10]
    #     new_text = []
    #
    #     for token in full_text:
    #         new_token = token
    #         if "http" in token and token in url:
    #             url_split = url.find("\":\"")
    #             long_url = url[url_split+3:]
    #             long_url = long_url[:len(long_url)-2]
    #             new_token = long_url
    #         new_text.append(new_token)
    #
    #     print(new_text)
    #     return ""

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        # self.handle_urls(doc_as_list)
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = remove_urls(doc_as_list[2])
        url = expand_url(doc_as_list[3])
        # url_indices = doc_as_list[4]
        retweet_text = remove_urls(doc_as_list[5])
        retweet_url = expand_url(doc_as_list[6])
        # retweet_url_indices = doc_as_list[7]
        quote_text = remove_urls(doc_as_list[8])
        quote_url = expand_url(doc_as_list[9])
        quote_url_indices = doc_as_list[10]
        retweet_quoted_text = remove_urls(doc_as_list[11])
        retweet_quoted_url = expand_url(doc_as_list[12])
        # retweet_quoted_url_indices = doc_as_list[13]
        term_dict = {}

        tokenized_text = self.parse_sentence(full_text)
        tokenized_urls = self.parse_sentence(url)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
