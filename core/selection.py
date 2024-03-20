from core.utils import loadpkl, savepkl
from core.conversion import os, multiple_ngram


def make_graph(files, mal_ngrams, graph_path, N=6):
    if os.path.exists(graph_path):
        graph = loadpkl(graph_path)
        return graph

    graph = dict()

    for file_idx, strings in enumerate(files):
        file_ngrams = multiple_ngram(strings, N=N)
        for ngram in file_ngrams:
            if ngram not in mal_ngrams:
                continue
            if ngram not in graph.keys():
                graph[ngram] = set()
            graph[ngram].add(file_idx)

    graph_list = []
    for ngram, file_set in graph.items():
        graph_list.append((ngram, file_set))

    savepkl(graph_path, graph_list)

    return graph_list


def get_representatives(graph, len_files, thetaD=1, thetaM=8):
    representatives = []
    file_matched = [0] * len_files

    k_satisfied = True
    buffer = []
    while graph:
        if k_satisfied:
            for ngram, file_set in graph:
                for file_idx in buffer:
                    file_set.discard(file_idx)
            graph.sort(key=lambda x: len(x[1]))

            k_satisfied = False
            buffer = []

        ngram, file_set = graph.pop()
        if len(file_set) < thetaM:
            break

        representatives.append(ngram)
        for file_idx in file_set:
            file_matched[file_idx] += 1

            if file_matched[file_idx] == thetaD:
                buffer.append(file_idx)
                k_satisfied = True

    return representatives
