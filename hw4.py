# Mirko Mantovani

import sys
import preprocess
import page_rank
import statistics
import os
import math

STOP_WORDS_PATH = './stopwords.txt'
DOCS_PATH = './www/abstracts/'
GOLD_PATH = './www/gold/'


def run_program():
    global current_doc
    documents = []
    idf = {}
    p_rank_max_iterations = 20

    # Point 1: word graph creation from documents
    tokenizer = preprocess.CustomTokenizer(STOP_WORDS_PATH)
    pageranker = page_rank.PageRank()
    for filename in os.listdir(DOCS_PATH):
        if not filename.startswith('.'):
            doc_text = open(DOCS_PATH + filename).read()

            # Point 1: word graph creation from documents
            # print('Point 1: word graph creation from documents')
            documents.append(tokenizer.tokenize(doc_text, idf))
            current_doc = documents[-1:][0]

            # Point 2: Running page rank on each word graph
            # print('Point 2: Running page rank on each word graph')
            current_doc.page_rank = pageranker.page_rank(current_doc.graph, p_rank_max_iterations)

            # Point 3: generating ngrams (1,2,3)grams and scoring them with the sum of the scores the page rank provides
            # print('Point 3: generating ngrams (1,2,3)grams')
            for n in range(1, 4):
                tokenizer.extract_ngrams(doc_text, current_doc, n)

            # Computing scores
            # print('Point 3: computing scores')
            for ng in current_doc.ngrams:
                words = ng.split(' ')
                for word in words:
                    if word in current_doc.page_rank:
                        current_doc.ngrams[ng] += current_doc.page_rank[word]

            # Point 4: MRR calculation
            gold_text = open(GOLD_PATH + filename).read()
            tokenizer.extract_gold_ngrams(gold_text, current_doc)
    # Computing idf
    for i in idf:
        idf[i] = math.log(len(documents) / idf[i], 2)
    # Computing tf-idf
    statistics.compute_tf_idf(idf, documents)
    for current_doc in documents:
        current_doc.ngrams_tf_idf = current_doc.ngrams.copy()
        for ng in current_doc.ngrams_tf_idf:
            current_doc.ngrams_tf_idf[ng] = 0
            words = ng.split(' ')
            for word in words:
                if word in current_doc.tf_idf:
                    current_doc.ngrams_tf_idf[ng] += current_doc.tf_idf[word]
    # Point 4: Computing and printing MRR
    statistics.compute_mrr(documents)
    # Point 5: Computing and printing MRR based on tf-idf
    statistics.compute_mrr(documents, with_tf_idf=True)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        STOP_WORDS_PATH = sys.argv[1]
        DOCS_PATH = sys.argv[2]
        GOLD_PATH = sys.argv[3]
    run_program()

