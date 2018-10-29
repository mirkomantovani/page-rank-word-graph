# Mirko Mantovani

import re
import string
import graph
import document
from nltk.stem import PorterStemmer


class CustomTokenizer:
    def __init__(self, path_stopwords=None, window=1):
        self.path_stopwords = path_stopwords
        self.tags_to_keep = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ']
        self.window = window
        self.stemmer = PorterStemmer()

        with open(self.path_stopwords, "r") as stop_file:
            self.stop_words = stop_file.readlines()

        self.stop_words = list(map(lambda x: x[:-1], self.stop_words))

    """
    Tokenizes a document
    """
    def tokenize(self, doc, vocabulary):
        word_count = {}
        G = graph.UndirectedGraph()
        tokens_in_window = []
        tokens = doc.split()
        for token in tokens:
            token_split = token.split("_")
            token = replace_digits(token_split[0]).lower()
            if token_split[1] not in self.tags_to_keep or token in self.stop_words:
                tokens_in_window = []
                continue
            self.stemmer.stem(token)
            if not token:
                continue
            if token not in word_count:
                if token not in vocabulary:
                    vocabulary[token] = 1
                else:
                    vocabulary[token] += 1
                G.add_node(token)
                word_count[token] = 1
            else:
                word_count[token] += 1
            if tokens_in_window:
                for token_in_window in tokens_in_window:
                    edge_weight = G.get_edge(token_in_window, token)
                    if edge_weight == -1:
                        G.add_edge(token_in_window, token, 1)
                    else:
                        G.add_edge(token_in_window, token, edge_weight + 1)
            tokens_in_window.append(token)
            if len(tokens_in_window) > self.window:
                tokens_in_window = tokens_in_window[1:]

        return document.Document(G, word_count)


# removing digits and returning the word
def replace_digits(st):
    return re.sub('\d', '', st)


# returns true if the word has less or equal 2 letters
def lesseq_two_letters(word):
    return len(word) <= 2


def preprocess(doc):
    # Splitting on whitespaces
    doc = doc.split()

    # Removing punctuations in words
    doc = [''.join(c for c in s if c not in string.punctuation) for s in doc]

    # Replace numbers with empty string
    doc = map(replace_digits, doc)

    # Removing empty words
    doc = [s for s in doc if s]

    # Removing words with len less or equal to 2
    doc = [s for s in doc if not lesseq_two_letters(s)]

    # Converting all words to lowercase
    doc = [x.lower() for x in doc]

    return doc
