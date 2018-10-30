# Mirko Mantovani

import preprocess
import page_rank
import os

STOP_WORDS_PATH = "./stopwords.txt"
DOCS_PATH = './www/abstracts/'

documents = []
vocabulary = {}

# Point 1: word graph creation from documents
tokenizer = preprocess.CustomTokenizer(STOP_WORDS_PATH)

# for filename in sorted(list(map(int, os.listdir(DOCS_PATH)))):
#     print(filename)

# docs = os.listdir(DOCS_PATH)
# docs = [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]
# for filename in sorted(list(map(int, [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]))):
#     print(filename)

for filename in list(map(str,sorted(list(map(int, [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]))))):
        documents.append(tokenizer.tokenize(open(DOCS_PATH + filename).read(), vocabulary))

pageranker = page_rank.PageRank()
p_rank = pageranker.page_rank(documents[0].graph, 100)

import operator
sorted_p = sorted(p_rank.items(), key=operator.itemgetter(1))

for i in sorted_p:
    print(i)
# for document in documents:
#     pageranker.page_rank(document.graph, 100)