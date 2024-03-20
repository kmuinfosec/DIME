import pickle
from ahocorapy.keywordtree import KeywordTree
import pandas as pd


def savepkl(path, file):
    with open(path, 'wb') as f:
        pickle.dump(file, f, pickle.HIGHEST_PROTOCOL)


def loadpkl(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


def visualization(query_string, signatures):

    kwtree = KeywordTree(case_insensitive=True)

    for ngram in signatures:
        kwtree.add(ngram)
    kwtree.finalize()

    concat_ngrams = []
    for string in query_string:
        res = list(kwtree.search_all(string))
        if res:
            concat_ngram = res[0][0]
            for idx, result in enumerate(res):
                if idx+1 < len(res):
                    if int(res[idx][1])+1 == int(res[idx+1][1]):
                        concat_ngram += str(res[idx+1][0][-1])
                    else:
                        concat_ngrams.append(concat_ngram)
                        concat_ngram = res[idx+1][0]
            concat_ngrams.append(concat_ngram)

    concat_ngrams.sort(key=lambda x: -len(x))

    return concat_ngrams


def calculate_metrics(row):
    accuracy_denominator = row['tp'] + row['tn'] + row['fp'] + row['fn']
    precision_denominator = row['tp'] + row['fp']
    recall_denominator = row['tp'] + row['fn']

    accuracy = None if accuracy_denominator == 0 else (
        row['tp'] + row['tn']) / accuracy_denominator
    precision = None if precision_denominator == 0 else row['tp'] / \
        precision_denominator
    recall = None if recall_denominator == 0 else row['tp'] / \
        recall_denominator
    f1_score = None

    if precision_denominator != 0 and recall_denominator != 0:
        f1_score = 2 * (precision * recall) / (precision + recall)

    return pd.Series({'accuracy': round(accuracy, 4) if accuracy is not None else None,
                      'precision': round(precision, 4) if precision is not None else None,
                      'recall': round(recall, 4) if recall is not None else None,
                      'f1_score': round(f1_score, 4) if f1_score is not None else None})
