# Mirko Mantovani

class Document:
    def __init__(self, document_graph, tf):
        # UndirectedGraph instance representing the word graph of the document
        self.graph = document_graph
        self.tf = tf
        self.tf_idf = {}
        self.ngrams = {}
        self.gold_ngrams = []
        self.page_rank = {}
