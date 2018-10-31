# Mirko Mantovani

import preprocess
import page_rank
import statistics
import os

STOP_WORDS_PATH = "./stopwords.txt"
DOCS_PATH = './www/abstracts/'
GOLD_PATH = './www/gold/'

documents = []
vocabulary = {}
p_rank_max_iterations = 10

# Point 1: word graph creation from documents
tokenizer = preprocess.CustomTokenizer(STOP_WORDS_PATH)
pageranker = page_rank.PageRank()

# for filename in sorted(list(map(int, os.listdir(DOCS_PATH)))):
#     print(filename)

# docs = os.listdir(DOCS_PATH)
# docs = [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]
# for filename in sorted(list(map(int, [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]))):
#     print(filename)

for filename in list(map(str, sorted(list(map(int, [i for i in os.listdir(DOCS_PATH) if not i.startswith(".")]))))):
        doc_text = open(DOCS_PATH + filename).read()

        # Point 1: word graph creation from documents
        print('Point 1: word graph creation from documents')
        documents.append(tokenizer.tokenize(doc_text, vocabulary))
        current_doc = documents[-1:][0]

        # Point 2: Running page rank on each word graph
        print('Point 2: Running page rank on each word graph')
        current_doc.page_rank = pageranker.page_rank(current_doc.graph, p_rank_max_iterations)

        # Point 3: generating ngrams (1,2,3)grams and scoring them with the sum of the scores the page rank provides
        print('Point 3: generating ngrams (1,2,3)grams')
        for n in range(1, 4):
            tokenizer.extract_ngrams(doc_text, current_doc, n)

        # Computing scores
        print('Point 3: computing scores')
        for ng in current_doc.ngrams:
            print(ng)
            words = ng.split(' ')
            print(words)
            for word in words:
                if word in current_doc.page_rank:
                    current_doc.ngrams[ng] += current_doc.page_rank[word]
                    print(current_doc.ngrams[ng])


        break;

# Point 4: MRR calculation
        gold_text = open(GOLD_PATH + filename).read()
        tokenizer.extract_gold_ngrams(gold_text, current_doc)
        statistics.compute_mrr(documents)


# Point 2: Running page rank on each word graph
# pageranker = page_rank.PageRank()
# p_rank = pageranker.page_rank(documents[0].graph, 100)
# import operator
# sorted_p = sorted(p_rank.items(), key=operator.itemgetter(1))
# for i in sorted_p:
#     print(i)


# for document in documents:
#     document.page_rank = pageranker.page_rank(document.graph, p_rank_max_iterations)
