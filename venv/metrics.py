import pandas as pd
from functools import reduce
import numpy

df = pd.DataFrame(
    {'query': [1, 1, 2, 2, 3], 'Tweet_id': [12345, 12346, 12347, 12348, 12349],
     'label': [1, 0, 1, 1, 0]})

test_number = 0
results = []


def get_query_dict(df):
    querys_result_dict={}
    querys = df["query"].tolist()
    for i in range(len(querys)):
        if querys[i] not in querys_result_dict.keys():
            querys_result_dict[querys[i]] = []
        querys_result_dict[querys[i]].append(i)
    return querys_result_dict


# precision(df, True, 1) == 0.5
# precision(df, False, None) == 0.5
def precision(df, single=False, query_number=None):
    """
        This function will calculate the precision of a given query or of the entire DataFrame
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param single: Boolean: True/False that tell if the function will run on a single query or the entire df
        :param query_number: Integer/None that tell on what query_number to evaluate precision or None for the entire DataFrame
        :return: Double - The precision
    """
    query_index=0
    last_query_index=len(df["query"])
    if single:
        try:
            query_index=df["query"].tolist().index(query_number)
            last_query_index=len(df["query"]) - df["query"].tolist()[::-1].index(query_number)
        except:
            print("invalid query index")
            return -1
    counter_of_querys = 0
    sum_of_precisions = 0
    query_val = df["query"][query_index]
    while query_index < last_query_index:
        label_sum = 0
        counter=0
        while query_index<last_query_index and query_val == df["query"][query_index]:
            counter += 1
            label_sum += df["label"][query_index]
            query_index += 1
        sum_of_precisions += (label_sum/counter)
        if query_index<last_query_index:
            query_val = df["query"][query_index]
        counter_of_querys += 1
    return sum_of_precisions/counter_of_querys


# recall(df, {1:2}, True) == 0.5
# recall(df, {1:2, 2:3, 3:1}, False) == 0.388
def recall(df, num_of_relevant):
    """
        This function will calculate the recall of a specific query or of the entire DataFrame
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param num_of_relevant: Dictionary: number of relevant tweets for each query number. keys are the query number and values are the number of relevant.
        :return: Double - The recall
    """
    querys_result_dict = get_query_dict(df)
    result = 0
    for query in num_of_relevant.keys():
        true_positve= sum(df["label"][querys_result_dict[query][0]: querys_result_dict[query][-1]+1])
        result += true_positve/num_of_relevant[query]
    return result/len(num_of_relevant.keys())


# precision_at_n(df, 1, 2) == 0.5
# precision_at_n(df, 3, 1) == 0
def precision_at_n(df, query_number=1, n=5):
    """
        This function will calculate the precision of the first n files in a given query.
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param query_number: Integer that tell on what query_number to evaluate precision
        :param n: Total document to splice from the df
        :return: Double: The precision of those n documents
    """
    querys_result_dict = get_query_dict(df) # {1: [0,1], 2: [2, 3], 3:[4]}  df["label] = [1, 0, 1, 1, 0]
    if query_number < 1 or query_number not in querys_result_dict.keys() or n > len(querys_result_dict[query_number]):
        print("invalid query index")
        return -1
    return sum(df["label"][querys_result_dict[query_number][0]: querys_result_dict[query_number][n-1]+1])/n



# map(df) == 2/3
def map(df):
    """
        This function will calculate the mean precision of all the df.
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :return: Double: the average precision of the df
    """
    querys_result_dict = get_query_dict(df)  # {1: [0,1], 2: [2, 3], 3:[4]}
    result = 0
    for query in querys_result_dict.keys():
        avg_precision = 0
        total_relevante_amuont = sum(df["label"][querys_result_dict[query][0]: querys_result_dict[query][-1]+1])
        n = 0
        for i in querys_result_dict[query]:
            n += 1
            if df["label"][i] == 1:
                avg_precision += precision_at_n(df, query, n)/total_relevante_amuont
        result += avg_precision/len(querys_result_dict.keys())
    return result



def test_value(func, expected, variables):
        """
            This function is used to test your code. Do Not change it!!
            :param func: Function: The function to test
            :param expected: Float: The expected value from the function
            :param variables: List: a list of variables for the function
        """
        global test_number, results
        test_number += 1
        result = func(*variables)
        try:
            result = float(f'{result:.3f}')
            if abs(result - float(f'{expected:.3f}')) <= 0.01:
                results.extend([f'Test: {test_number} passed'])
            else:
                results.extend([f'Test: {test_number} Failed running: {func.__name__}'
                                f' expected: {expected} but got {result}'])
        except ValueError as ve:
            results.extend([f'Test: {test_number} Failed running: {func.__name__}'
                            f' value return is not a number'])
        except:
            d = traceback.format_exc().splitlines()
            results.extend([f'Test: {test_number} Failed running: {func.__name__} with the following error: {" ".join(d)}'])


test_value(precision, 0.5, [df, True, 1])
test_value(precision, 0.5, [df, False, None])
test_value(recall, 0.5, [df, {1: 2}])
test_value(recall, 0.388, [df, {1: 2, 2: 3, 3: 1}])
test_value(precision_at_n, 0.5, [df, 1, 2])
test_value(precision_at_n, 0, [df, 3, 1])
test_value(map, 2 / 3, [df])
for res in results:
    print(res)
