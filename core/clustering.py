from sklearn.cluster import DBSCAN

def clustering(graph, representatives, len_file, eps=0.5, min_samples=5):
    dataset = [set() for _ in range(len_file)]
    ngrams = []
    ngram_idx = 0

    for ngram, file_set in graph:
        if ngram not in representatives:
            continue

        for file_idx in file_set:
            dataset[file_idx].add(ngram_idx)

        ngram_idx += 1
        ngrams.append(ngram)

    vectors = []
    for idx, words in enumerate(dataset):
        vector = [0] * ngram_idx
        for word in words:
            vector[word] = 1
        vectors.append(vector)

    model = DBSCAN(eps=eps, min_samples=min_samples,
                   metric='cosine').fit(vectors)

    wordset = []
    for data in dataset:
        tmp_ngrams = set()
        for idx in data:
            tmp_ngrams.add(ngrams[idx])
        wordset.append(tmp_ngrams)

    return model.labels_, wordset