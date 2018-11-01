import document
from heapq import nlargest


def compute_mrr(documents):
    MRR = {}
    for k in range(1, 11):
        MRR[k] = 0
        for doc in documents:
            top = nlargest(k, doc.ngrams, key=doc.ngrams.get)
            r = 0
            rankd = 0
            for index, t in enumerate(top):
                if t in doc.gold_ngrams:
                    rankd = index +1
                    break
            if rankd:
                MRR[k] = MRR[k] + 1 / rankd
        MRR[k] = MRR[k] / len(doc.n_gold_standards)
        print('MRR when looking at the top {} words: {}'.format(k, MRR[k]))
        with open('MRR.txt', 'a') as text_file:
            text_file.write('{}\n'.format(MRR[k]))