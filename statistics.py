import document
from heapq import nlargest


def compute_mrr(documents, with_tf_idf=False):
    MRR = {}
    for k in range(1, 11):
        # print(k)
        # print()
        MRR[k] = 0
        for doc in documents:
            if with_tf_idf:
                top = nlargest(k, doc.tf_idf, key=doc.tf_idf.get)
            else:
                top = nlargest(k, doc.ngrams, key=doc.ngrams.get)
            rankd = 0
            # print(doc)
            # print(top)
            for index, t in enumerate(top):
                # print("is "+t + "in " + str(doc.gold_ngrams))
                if t in doc.gold_ngrams:
                    # print(t + " is in " + str(doc.gold_ngrams))
                    rankd = index +1
                    break
            if rankd:
                MRR[k] = MRR[k] + 1 / rankd
        MRR[k] = MRR[k] / len(documents)
        print('MRR when looking at the top {} words: {}'.format(k, MRR[k]))
        with open('MRR.txt', 'a') as text_file:
            text_file.write('{}\n'.format(MRR[k]))


def compute_tf_idf(idf, documents):
    for doc in documents:
        for word in doc.tf:
            doc.tf_idf[word] = doc.tf[word] * idf[word]

