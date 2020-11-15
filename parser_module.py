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


def parse_hashtags(hashtag): #problems: USE will translate to  u,s,a and all so
    list_of_hashtags = []
    if hashtag.find(".") > 0:
        hashtag = hashtag[0:hashtag.find(".")]
    list_of_hashtags.append(hashtag.lower())
    i = 2
    j = 1
    while i <= len(hashtag):
        if i == len(hashtag) or hashtag[i].isupper() or hashtag[i] == "_":
            list_of_hashtags.append(hashtag[j:i].lower())
            if i == len(hashtag) or hashtag[i].isupper():
                j = i
            else:
                j = i + 1
        i += 1
    return list_of_hashtags


def parse_number(num, suffix):
    num = float(num)
    if suffix.find('/') > 0:
        return str(num) + " " + suffix
    ch = ""
    num = get_suffix(num, suffix)
    if 1000 <= num < 1000000:
        num /= 1000
        ch = "K"
    elif 1000000 <= num < 1000000000:
        num /= 1000000
        ch = "M"
    elif num >= 1000000000:
        num /= 1000000000
        ch = "B"
    if num.is_integer():
        num = int(num)
    else:
        num = round(num, 3)
    return str(num) + ch


def get_suffix(num, suffix):
    if suffix == "Thousand":
        num *= 1000
    elif suffix == "Million":
        num *= 1000000
    elif suffix == "Billion":
        num *= 1000000000
    return num




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




    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
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
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
