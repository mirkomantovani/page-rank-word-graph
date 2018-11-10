import document
from heapq import nlargest


def compute_mrr(documents, with_tf_idf=False):
    print()
    if with_tf_idf:
        print("Computing MRR with TF-IDF")
    else:
        print("Computing MRR")
    MRR = {}
    for k in range(1, 11):
        # print(k)
        # print()
        MRR[k] = 0
        i=0
        for doc in documents:
            i=i+1
            #print(i)
            if with_tf_idf:
                top = nlargest(k, doc.ngrams_tf_idf, key=doc.ngrams_tf_idf.get)
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
        if with_tf_idf:
            print('Using top-{} words, MRR using TF-IDF: {}'.format(k, MRR[k]))
        else:
            print('Using top-{} ngrams, MRR: {}'.format(k, MRR[k]))


def compute_tf_idf(idf, documents):
    for doc in documents:
        for word in doc.tf:
            doc.tf_idf[word] = doc.tf[word] * idf[word]

