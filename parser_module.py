from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document


def remove_urls(full_text):
    if not full_text:
        return
    split = full_text.split(' ')
    clean = [token for token in split if "http" not in token.lower()]
    return ' '.join(clean)


def tokenize_url(url):
    if not url:
        return
    url_split = url.find("\":\"")
    if url_split == -1:
        return
    long_url = url[url_split + 3:]
    long_url = long_url[:len(long_url) - 2]
    tokenized_url = long_url.replace('/', '.').replace('-', '.').split('.')
    return tokenized_url


def parse_hashtags(hashtag):  # problems: USE will translate to  u,s,a and all so
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
        text_tokens_without_stopwords = [w.lower() if w[0].islower() else w.upper() for w in text_tokens if w not in self.stop_words]
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url_tokens = tokenize_url(doc_as_list[3])
        # url_indices = doc_as_list[4]
        retweet_text = doc_as_list[5]
        retweet_url_tokens = tokenize_url(doc_as_list[6])
        # retweet_url_indices = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url_tokens = tokenize_url(doc_as_list[9])
        quote_url_indices = doc_as_list[10]
        retweet_quoted_text = doc_as_list[11]
        retweet_quoted_url_tokens = tokenize_url(doc_as_list[12])
        # retweet_quoted_url_indices = doc_as_list[13]
        term_dict = {}

        preprocessed = self.pre_process(full_text)
        full_text = preprocessed[0]
        tokenized_text = preprocessed[1]

        # if retweet_text:
        #     preprocessed = self.pre_process(retweet_text)
        #     retweet_text = preprocessed[0]
        #     tokenized_text.extend(preprocessed[1])

        if quote_text:
            preprocessed = self.pre_process(quote_text)
            quote_text = preprocessed[0]
            tokenized_text.extend(preprocessed[1])

        tokenized_text.extend(self.parse_sentence(full_text))
        # tokenized_text.extend(self.parse_sentence(retweet_text))
        if quote_text:
            tokenized_text.extend(self.parse_sentence(quote_text))

        if url_tokens:
            tokenized_text.extend(url_tokens)
        if retweet_url_tokens:
            tokenized_text.extend(retweet_url_tokens)
        if quote_url_tokens:
            tokenized_text.extend(quote_url_tokens)

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url_tokens, retweet_text, retweet_url_tokens, quote_text,
                            quote_url_tokens, term_dict, doc_length)
        return document

    def pre_process(self, text):
        if not text:
            return
        tokens_list = []
        clean_text = []
        text = text.replace("percentage", "percent")
        split = text.split(' ')
        for i in range(len(split)):
            token = split[i]
            try:
                # HASHTAGS
                if token[0] == '#':
                    tokens_list.append(self.parse_hashtags(token))

                # TAGS
                elif token[0] == '@':
                    tokens_list.append(token if not token.endswith(':') else token[:len(token)-1])

                # PERCENTAGES
                elif i < len(split) - 1 and split[i + 1] == "percent":
                    number = float(token)
                    if token.isnumeric():  # token is a round number
                        tokens_list.append(token + "%")
                    else:  # token is a float number
                        tokens_list.append(str(number) + "%")
                elif token.endswith('%'):
                    number = float(token[:token.find('%')])
                    tokens_list.append(token)

                # NUMBERS
                elif token.replace(',', '').replace('.', '').isnumeric():
                    number = token.replace(',', '')
                    if i < len(split) - 1:
                        next_token_used, number = parse_number(number, split[i + 1])
                        tokens_list.append(number)
                        if next_token_used:
                            i += 1
                    else:
                        tokens_list.append(parse_number(number, ""))

                elif "http" in token.lower():
                    continue
                # ALL THE REST - REGULAR TOKENS
                else:
                    clean_text.append(token)
            except:
                clean_text.append(token)

        return ' '.join(clean_text), tokens_list
