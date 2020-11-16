import re

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
    # for w in tokenized_url:
    #     print(w[0])
    return [w.lower() if (len(w) > 0 and w[0].islower()) else w.upper() for w in tokenized_url]


def parse_hashtags(hashtag):  # problems: USA will translate to  u,s,a and all so
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
        return str(num) + " " + suffix, True
    ch = ""
    num, flag = get_suffix(num, suffix)
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
    return str(num) + ch, flag


def get_suffix(num, suffix):
    flag = False
    suffix = suffix.lower()
    if suffix == "thousand":
        num *= 1000
        flag = True
    elif suffix == "million":
        num *= 1000000
        flag = True
    elif suffix == "billion":
        num *= 1000000000
        flag = True
    return num, flag


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')


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
        quote_text = doc_as_list[8]
        quote_url_tokens = tokenize_url(doc_as_list[9])

        # url_indices = doc_as_list[4]
        # retweet_text = doc_as_list[5]
        # retweet_url_tokens = tokenize_url(doc_as_list[6])
        # retweet_url_indices = doc_as_list[7]
        # quote_url_indices = doc_as_list[10]
        # retweet_quoted_text = doc_as_list[11]
        # retweet_quoted_url_tokens = tokenize_url(doc_as_list[12])
        # retweet_quoted_url_indices = doc_as_list[13]

        term_dict = {}

        tokenized_text = self.parse_text(full_text)
        if quote_text:
            tokenized_text.extend(self.parse_text(quote_text))

        if url_tokens:
            tokenized_text.extend(url_tokens)
        if quote_url_tokens:
            tokenized_text.extend(quote_url_tokens)

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            if len(term) == 0:
                continue
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        # document = Document(tweet_id, tweet_date, full_text, url_tokens, retweet_text, retweet_url_tokens, quote_text,
        #                     quote_url_tokens, term_dict, doc_length)
        document = Document(tweet_id, term_dict)
        return document

    def parse_text(self, text):
        if not text:
            return
        tokens_list = []
        clean_text = ""

        # split = text.split(' ')
        split = re.sub('(\.)(\.)(\.)*|[!$%^&?*()={}~`]+|\[|\]', r' ', text).split()

        for i in range(len(split)):
            token = split[i]
            if not token.isascii() or "http" in token.lower():
                continue
            try:
                # HASHTAGS
                if token[0] == '#':
                    tokens_list.extend(parse_hashtags(token))

                # TAGS
                elif token[0] == '@':
                    tokens_list.append(token.lower() if not token.endswith(':') else token[:len(token)-1].lower())

                # PERCENTAGES
                elif i < len(split) - 1 and split[i + 1] in ["percent", "percentage"]:
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
                        number, next_token_used = parse_number(number, split[i + 1])
                        tokens_list.append(number)
                        if next_token_used:
                            i += 1
                    else:
                        number, next_token_used = parse_number(number, "")
                        tokens_list.append(number)

                # ALL THE REST - REGULAR TOKENS
                else:
                    clean_text += token + " "
            except:
                clean_text += token + " "

        # tokenizer = word_tokenize(clean_text)
        # tokenizer2 = clean_text.split(' ')

        # tokens_list.extend(word_tokenize(clean_text))
        tokens_list.extend(clean_text.split(' '))
        text_tokens_without_stopwords = [w.lower() if len(w) > 0 and w[0].islower() else w.upper()
                                         for w in tokens_list if w not in self.stop_words]

        return text_tokens_without_stopwords
