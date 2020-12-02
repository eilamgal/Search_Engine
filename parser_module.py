import calendar
from datetime import datetime

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from document import Document
import re
import spacy
from nltk import PorterStemmer
import time


def remove_urls(full_text):
    if not full_text:
        return
    split = full_text.split(' ')
    clean = [token for token in split if "http" not in token.lower()]
    return ' '.join(clean)


def tokenize_url(url):
    if url == "{}" or url is None:
        return None, "0"
    url_split = url.find("\":\"")
    if url_split == -1:
        return
    long_url = url[url_split + 3:]
    long_url = long_url[:len(long_url) - 2]
    # tokenized_url = long_url.replace('/', '.').replace('-', '.').split('.')
    tokenized_url = re.sub(r'([#!$%^&?*()={}~`\[\]])|([&=#/\.:\-_]+)', r' \1', long_url).split()

    referral_id = "0"
    if len(tokenized_url) >= 2:
        if (tokenized_url[len(tokenized_url) - 2] == "status"
                and tokenized_url[len(tokenized_url) - 1].isnumeric()):
            referral_id = tokenized_url[len(tokenized_url) - 1]
            del tokenized_url[len(tokenized_url) - 1]

    # for w in tokenized_url:
    #     print(w[0])
    return [w.lower() if (len(w) > 0 and w[0].islower()) else w.upper() for w in tokenized_url if
            w.isascii()], referral_id


def parse_hashtags(hashtag):  # problems: USA will translate to  u,s,a and all so
    if hashtag.find(".") > 0:
        hashtag = hashtag[0:hashtag.find(".")]
    list_of_tokens = [hashtag.lower()]
    if hashtag.find("_") > 0:
        list_of_tokens.extend(
            token.lower() for token in re.sub('([_][a-z]+)', r' ', re.sub('([_]+)', r' ', hashtag[1:])).split())
    else:
        list_of_tokens.extend(
            token.lower() for token in re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', hashtag[1:])).split())
    return list_of_tokens


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
        # self.entities = spacy.load('en_core_web_sm')
        self.porter = PorterStemmer()
        self.stem = True

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url_tokens = tokenize_url(doc_as_list[3])[0]
        quote_text = doc_as_list[8]
        quote_url_tokens, referral_id1 = tokenize_url(doc_as_list[9])
        retweet_url_tokens, referral_id2 = tokenize_url(doc_as_list[6])
        referrals = {referral_id1, referral_id2}

        months = {month: index for index, month in enumerate(calendar.month_abbr) if month}
        split_date = tweet_date.split(' ')
        tweet_timestamp = int(datetime(int(split_date[5]), months[split_date[1]], int(split_date[2])))

        if tweet_id in referrals:
            referrals.remove(tweet_id)
        if referrals == {'0'}:
            referrals = None
        elif '0' in referrals:
            referrals.remove('0')

        # REDUNDANT PARAMETERS (for now)
        # url_indices = doc_as_list[4]
        # retweet_text = doc_as_list[5]
        # retweet_url_tokens = tokenize_url(doc_as_list[6])
        # retweet_url_indices = doc_as_list[7]
        # quote_url_indices = doc_as_list[10]
        # retweet_quoted_text = doc_as_list[11]
        # retweet_quoted_url_tokens = tokenize_url(doc_as_list[12])
        # retweet_quoted_url_indices = doc_as_list[13]

        term_dict = {}

        tokenized_text, entities = self.parse_text(full_text)
        if quote_text:
            parsed_quote = self.parse_text(quote_text)
            tokenized_text.extend(parsed_quote[0])
            entities.extend(parsed_quote[1])

        if url_tokens:
            tokenized_text.extend(url_tokens)
        if quote_url_tokens:
            tokenized_text.extend(quote_url_tokens)
        if retweet_url_tokens:
            tokenized_text.extend(retweet_url_tokens)
        """
        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:
            # temporary solutions
            if len(term) < 2:
                continue
            if term[len(term) - 1] == ".":
                term = term[0:len(term) - 1]
            # Cats are good. bay cats => {(Cats ,1)}
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        """
        tweet_length = len(tokenized_text)
        for term in tokenized_text:
            if len(term) < 2:
                continue
            if term[len(term) - 1] == ".":
                term = term[0:len(term) - 1]
            if term.lower() not in term_dict.keys() and term.upper() not in term_dict.keys():
                term_dict[term] = 1
            elif term.isupper() and term.lower() in term_dict.keys():
                term_dict[term.lower()] += 1
            elif term.islower() and term.upper() in term_dict.keys():
                term_dict[term] = term_dict[term.upper()] + 1
                del term_dict[term.upper()]
            else:
                term_dict[term] += 1

        entities_dict = {}

        for entity in entities:
            if len(entity) < 2 or not entity.isascii():
                continue
            if entity not in entities_dict.keys():
                entities_dict[entity] = 1
            else:
                entities_dict[entity] += 1

        # document = Document(tweet_id, tweet_date, full_text, url_tokens, retweet_text, retweet_url_tokens, quote_text,
        #                     quote_url_tokens, term_dict, doc_length)
        document = Document(tweet_id=tweet_id, tweet_timestamp=tweet_timestamp, term_doc_dictionary=term_dict,
                            entities_doc_dictionary=entities_dict, referral_ids=referrals, tweet_length=tweet_length)
        return document

    def parse_text(self, text):
        if not text:
            return
        tokens_list = []
        clean_text = ""
        # split = text.split(' ')
        if text[0:2] == "RT":
            text = text[2:]
        entities = [x.group() for x in re.finditer(r'[A-Z]+[a-z]+([\s\-]+[A-Z]+[a-z]+)+', text)]
        split = re.sub(r'(\.)(\.)(\.)*|[!$%^&?*()={}~`]+|\[|\]', r' \1', text).split()

        for i in range(len(split)):
            token = split[i]
            if not token.isascii() or "http" in token.lower() or len(token) == 0:
                continue
            try:
                if token.isalpha():
                    clean_text += token + " "
                # HASHTAGS
                elif token[0] == '#':
                    tokens_list.extend(parse_hashtags(token))

                # TAGS
                elif token[0] == '@':
                    tokens_list.append(token if not token.endswith(':') else token[:len(token) - 1].lower())

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

        tokens_list.extend(clean_text.split(' '))

        text_tokens_without_stopwords = []

        if self.stem:
            text_tokens_without_stopwords = [self.porter.stem(w).lower() if w[0].islower()
                                             else self.porter.stem(w).upper()
                                             for w in tokens_list if len(w) > 0 and w not in self.stop_words]
        else:
            text_tokens_without_stopwords = [w.lower() if w[0].islower()
                                             else w.upper()
                                             for w in tokens_list if len(w) > 0 and w not in self.stop_words]

        return text_tokens_without_stopwords, entities
