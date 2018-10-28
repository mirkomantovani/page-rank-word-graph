# coding: utf-8

# # Information Retrieval HW2 - Mirko Mantovani - 14 September 2018
# The homework consists in creating an inverted index based on some documents in a corpus,
# then, using cosine similarity and tf-idf representation, retrieving relevant documents for
# each of a set of query, ranked by the most relevant to the least one

import operator
import os
from collections import Counter

from preprocess import *
from tabulate import tabulate
from nltk.stem import PorterStemmer
import math

RELEVANCE_PATH = "./relevance.txt"
QUERIES_PATH = './queries.txt'
STOP_WORDS_PATH = "./stopwords.txt"
DOCS_PATH = './cranfieldDocs/'

words = []
n_docs = 0
documents = []

# Specific preprocessing

# Tokenization This tokenization preprocessing does this: splits on whitespaces, then removes the punctuations on
# each obtained word, removes empty words, words containing numbers, words consisting of one letter other than 'a',
# 'A', or 'I', because they cannot be considered english words. Finally it converts all the words to lowercase in
# order for the following statistics to be meaningful. Of course many other words will not be real words but it is
# not requested to remove them in this exercise.

# This function removes all SGML tags and retain everything else
def remove_SGML_tags(doc):
    return re.sub('<[/]?[A-Z]*>', '', doc)


# This function returns title and text of a document
def get_title_text(doc):
    return remove_SGML_tags(
        re.search('<TITLE>.*</TITLE>', doc, flags=re.DOTALL).group() + re.search('<TEXT>.*</TEXT>', doc,
                                                                                 flags=re.DOTALL).group())


for filename in sorted(os.listdir(DOCS_PATH)):
    if not filename.startswith('.'):
        documents.append(preprocess(get_title_text(open('cranfieldDocs/' + filename).read())))
    else:
        print(filename)

n_docs = len(documents)
# print('preprocessed docs: ' + str(n_docs))

# ## Stemming and stop-words elimination
# A stop-word elimination is needed even before the stemming because some stop-words could be stemmed
# and become non-stop-words, i.e. "has" -> "ha", "anyone" -> "anyon"

with open(STOP_WORDS_PATH, "r") as stop_file:
    stop_words = stop_file.readlines()

stop_words = list(map(lambda x: x[:-1], stop_words))

for i in range(n_docs):
    documents[i] = [s for s in documents[i] if s not in stop_words]

# ### Applying Porter Stemming

ps = PorterStemmer()


def stem(word):
    return ps.stem(word)


for i in range(n_docs):
    documents[i] = list(map(stem, documents[i]))

# ### Reapplying stop-words elimination

for i in range(n_docs):
    documents[i] = [s for s in documents[i] if s not in stop_words]

# # Inverted Index

# my inverted index is a python dictionary whose key are the words, it retrieves another dictionary indexed with
# doc number (already incremented by one so that it is the actual document cranfieldXXXX with XXXX the index of
# the inner dictionary)
inverted_index = {}

for doc in range(n_docs):
    for word in documents[doc]:
        inverted_index.setdefault(word, {})[doc + 1] = inverted_index.setdefault(word, {}).get(doc + 1, 0) + 1

# testing correctness
# def sumfrequences(word):
#    s = 0
#    for doc in inverted_index[word]:
#        s += inverted_index[word][doc]
#    return s
# sum = 0
# for w in inverted_index.keys():
#    sum += sumfrequences(w)
# sum
# 112897


# ### Unique words

len(inverted_index.keys())


# document frequency = number of docs containing a specific word, dictionary with key = word, value = num of docs
df = {}
# inverse document frequency
idf = {}

for key in inverted_index.keys():
    df[key] = len(inverted_index[key].keys())
    idf[key] = math.log(n_docs / df[key], 2)


def tf_idf(word, doc):
    return inverted_index[word][doc] * idf[word]


# # Queries preprocessing

queries = []

with open(QUERIES_PATH) as f:
    for q in f.read().splitlines():
        queries.append(preprocess(q))

n_queries = len(queries)

for i in range(n_queries):
    # first stop-word elimination
    queries[i] = [s for s in queries[i] if s not in stop_words]
    # stemming
    queries[i] = list(map(stem, queries[i]))
    # second stop-word elimination
    queries[i] = [s for s in queries[i] if s not in stop_words]


# # Computing cosine similarity for a query and each document

def inner_product_similarities(query):
    # dictionary in which I'll sum up the similarities of each word of the query with each document in
    # which the word is present, key is the doc number,
    # value is the similarity between query and document
    similarity = {}
    for word in query:
        wq = idf.get(word, 0)
        if wq != 0:
            for doc in inverted_index[word].keys():
                similarity[doc] = similarity.get(doc, 0) + tf_idf(word, doc) * wq
    return similarity


def doc_length(doc):
    # possibilities: if a word is present 2 times, do (tf_idf *2)^2, or, more likely, since the frequency is already
    # accounted for in tf, just use tf_idf^2 and keep track that you already summed that word contribution. CASE 2:to
    #  keep track of the words already accounted for I'll create a temporary list
    words_accounted_for = []
    # since it would be inefficient to scan the inverted index to find all the words in a document I'll reuse the
    # initial data structure containing docs
    length = 0
    # i think the error is here, tf already accounts for a word that appears more times, but Im summing more times
    # anyway here yes this is an error
    for word in documents[doc - 1]:
        if word not in words_accounted_for:
            length += tf_idf(word, doc) ** 2
            words_accounted_for.append(word)
    return math.sqrt(length)


def query_length(query):
    # IMPORTANT: in this HW no query has repeated words, so I can skip the term frequency calculation
    # for the query, and just use idfs quared
    length = 0
    cnt = Counter()
    for w in query:
        cnt[w] += 1
    for w in cnt.keys():
        length += (cnt[w]*idf.get(word, 0)) ** 2
    return math.sqrt(length)


def cosine_similarities(query):
    similarity = inner_product_similarities(query)
    for doc in similarity.keys():
        similarity[doc] = similarity[doc] / doc_length(doc) / query_length(query)
    return similarity


def rank_docs(similarities):
    return sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)


# ## Final Data structure containing ranked docs by similarities for each query

# ranked similarities is a dictionary indexed with the number of the query starting with 1 up to n_queries,
# the values are the list of ranked documents by cosine similarity based on that specific query, in particular,
# each document row is a list with doc number and cosine similarity wrt the query
ranked_similarities = {}
for query in range(n_queries):
    ranked_similarities[query + 1] = rank_docs(cosine_similarities(queries[query]))

# for i in range(n_queries):
#     print("Relevant docs for query " + str(i + 1) + ": " + str(len(ranked_similarities[i + 1])))

# ## Computing precision and recall considering 10,50,100,500 top docs retrieved


with open(RELEVANCE_PATH, "r") as rel:
    relevant_docs = rel.readlines()

relevant_docs = list(map(lambda x: x[:-1], relevant_docs))

# creating dictionary relevant_for_query indexed by query number, outputs the list of relevant docs
relevant_for_query = {}
for line in relevant_docs:
    relevant_for_query[int(line.split()[0])] = relevant_for_query.get(int(line.split()[0]), [])
    relevant_for_query[int(line.split()[0])].append(int(line.split()[1]))


def get_docs_from_tuples(list_lists):
    """Retrieves the docs from a list of lists in which the first element of the inner list is the doc"""
    docs = []
    for l in list_lists:
        docs.append(l[0])

    return docs


def intersection(l1, l2):
    return list(set(l1) & set(l2))


# passing the query number, the list of relevant documents for that query and the number of docs to take into
# consideration it accesses the ranked_similarities and returns the precision
def precision(query_n, relevant_d, n_docs):
    """precision is number of relevant docs retrieved / total num of docs retrieved, the number of relevant docs retrieved
    is only from the first n_docs documents in this case, so I only need to do the intersection between the relevant_d
    and this subset that is the first n_docs in ranked_similarities (ranked_similarities[query_n][:n_docs])"""
    n_rel_docs = len(intersection(get_docs_from_tuples(ranked_similarities[query_n][:n_docs]), relevant_d))
    return n_rel_docs / n_docs


def recall(query_n, relevant_d, n_docs):
    """the nominator of recall is the same as precision, the denominator instead is the total number of relevant docs, which
    is just len(relevant_d)"""
    n_rel_docs = len(intersection(get_docs_from_tuples(ranked_similarities[query_n][:n_docs]), relevant_d))
    return n_rel_docs / len(relevant_d)


retrieved_n = [10, 50, 100, 500]
# for q in range(1, n_queries + 1):
#     for n in retrieved_n:
#         print('Query: ' + str(q) + ', num retrieved: ' + str(n) + ', Precision: ' + str(
#             precision(q, relevant_for_query[q], n)) + ', Recall: '
#               + str(recall(q, relevant_for_query[q], n)))


p = 0
r = 0
for n in retrieved_n:
    avg_prec = 0
    avg_rec = 0
    pr = []
    print('Top ' + str(n) + ' documents in rank list')
    for q in range(1, n_queries + 1):
        p = precision(q, relevant_for_query[q], n)
        r = recall(q, relevant_for_query[q], n)
        avg_prec += p
        avg_rec += r
        pr.append(['Query: ' + str(q), ' Precision: ' + str(p), ' Recall: ' + str(r)])
    print(tabulate(pr))
    print('Average precision: ' + str(avg_prec / n_queries) + ', average recall: ' + str(avg_rec / n_queries))
    print("")
