
import graph


class Document:
    def __init__(self, document_graph, word_count):
        # UndirectedGraph instance representing the word graph of the document
        self.graph = document_graph
        self.word_count = word_count
