import math

def make_signature(file_ngrams, cluster_labels, delta, WL=set()):
    label_cnt = dict()
    ngram_freq = dict()
    for file_idx, label in enumerate(cluster_labels):
        if label == -1:
            continue
        if label not in ngram_freq.keys():
            ngram_freq[label] = dict()
            label_cnt[label] = 0

        label_cnt[label] += 1
        for ngram in file_ngrams[file_idx]:
            if ngram not in ngram_freq[label].keys():
                ngram_freq[label][ngram] = 1
            else:
                ngram_freq[label][ngram] += 1

    signatures = dict()
    for label in label_cnt.keys():
        sig = {x for x, y in ngram_freq[label].items() if y >= int(
            math.ceil(delta * label_cnt[label]))}
        sig -= WL
        signatures[label] = [sig, label_cnt[label]]

    return sorted(list(signatures.items()), key=lambda x: x[1][1])