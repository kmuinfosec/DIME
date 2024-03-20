import os
import re
from tqdm.auto import tqdm


def extract_string(path, min_bytes=6):
    with open(os.path.join(path), 'rb') as f:
        file_data = f.read()
        string = set(s.decode() for s in re.findall(
            b"[\x20-\x7e]{" + bytes(str(min_bytes), 'utf-8') + b",}", file_data))
    return string


def multiple_extract_string(path, min_bytes=6):
    strings = dict()
    for file in tqdm(os.listdir(path), desc='extract strings'):
        strings[file] = extract_string(
            os.path.join(path, file), min_bytes=min_bytes)
    return strings


def multiple_ngram(strings, N=6):
    ngrams = set()
    for string in strings:
        ngrams |= Ngram(string, N=N)
    return ngrams


def Ngram(string, N=6):
    ngram = set()
    for i in range(len(string) - N + 1):
        ngram.add(string[i:i+N])
    return ngram


def make_whitelist(file_strings: str, N=6, thetaB=1):
    ngram_frequency = dict()
    for strings in tqdm(file_strings, desc="Creating whitelist"):
        ngrams = multiple_ngram(strings, N=N)
        for ngram in ngrams:
            if ngram not in ngram_frequency.keys():
                ngram_frequency[ngram] = 1
            else:
                ngram_frequency[ngram] += 1

    white_list = set(
        [key for key, value in ngram_frequency.items() if value >= thetaB])

    return white_list
