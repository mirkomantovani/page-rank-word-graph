# Mirko Mantovani

import preprocess
import os

STOP_WORDS_PATH = "./stopwords.txt"
DOCS_PATH = './www/abstracts/'

documents = []
vocabulary = {}

# Point 1: word graph creation from documents
tokenizer = preprocess.CustomTokenizer(STOP_WORDS_PATH)

for filename in sorted(os.listdir(DOCS_PATH)):
    if not filename.startswith('.'):
        documents.append(tokenizer.tokenize(open(DOCS_PATH + filename).read(), vocabulary))

