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

        # words considered adjacent if at most at length = window, if window = 1 only strictly adjacent words are adj
        self.window = window
        self.stemmer = PorterStemmer()

        with open(self.path_stopwords, "r") as stop_file:
            self.stop_words = stop_file.readlines()

        self.stop_words = list(map(lambda x: x[:-1], self.stop_words))

    def extract_ngrams(self, doc_text, document, length =1):
        tokens_in_window = []
        tokens = doc_text.split()
        for token in tokens:
            token_split = token.split("_")
            # token = replace_digits(token_split[0]).lower() nope, digits are needed for instance for the word P2P
            token = token_split[0].lower()
            if token_split[1] not in self.tags_to_keep or token in self.stop_words:
                tokens_in_window = []
                continue
            token = self.stemmer.stem(token)
            tokens_in_window.append(token)
            if len(tokens_in_window) > length:
                tokens_in_window = tokens_in_window[1:]
                # considering only length-grams
            ng = ''
            if len(tokens_in_window) == length:
                for t in tokens_in_window:
                    ng += t+' '
                ng = ng[:-1]
            if ng:
                # define new ngram for document and set to 0 its initial score
                document.ngrams[ng] = 0

# maybe also remove stopwords here since there was an 'and'
#     hypertext / hypermedia in 19653
    def extract_gold_ngrams(self, doc_text, document):
        lines = doc_text.split('\n')
        lines = lines[:-1]
        for line in lines:
            tokens = line.split(' ')
            ng = ''
            for token in tokens:
                t = self.stemmer.stem(token.lower())
                if t not in self.stop_words:
                    ng += t+' '
            ng = ng[:-1]
            if ng:
                # define new ngram for document and set to 0 its initial score
                document.gold_ngrams.append(ng)
        #         print(ng)
        # print(document.gold_ngrams)


    """
    Tokenizes a document and builds the word graph
    """
    def tokenize(self, doc_text, idf):
        tf = {}
        G = graph.UndirectedGraph()
        tokens_in_window = []
        tokens = doc_text.split()
        for token in tokens:
            token_split = token.split("_")
            # token = replace_digits(token_split[0]).lower() nope, digits are needed for instance for the word P2P
            token = token_split[0].lower()
            if token_split[1] not in self.tags_to_keep or token in self.stop_words:
                tokens_in_window = []
                continue
            token = self.stemmer.stem(token)
            if not token:
                continue
            if token not in tf:
                if token not in idf:
                    idf[token] = 1
                else:
                    idf[token] += 1
                G.add_node(token)
                tf[token] = 1
            else:
                tf[token] += 1
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

        return document.Document(G, tf)


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
