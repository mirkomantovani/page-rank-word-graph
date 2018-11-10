# Mirko Mantovani

class Document:
    def __init__(self, document_graph, tf):
        # UndirectedGraph instance representing the word graph of the document
        self.graph = document_graph
        self.tf = tf
        self.tf_idf = {}
        self.ngrams = {}
        #same as ngrams but the value (score( is based on tf-idf
        self.ngrams_tf_idf = {}
        self.gold_ngrams = []
        self.page_rank = {}
