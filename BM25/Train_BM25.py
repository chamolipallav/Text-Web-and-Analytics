import math
from stemming.porter2 import stem
import sys, os, coll, df

def avg_doc_len(coll):

    return 

def BM25_Train(coll, bench, theta):
    T = {}

    #selecting positive documents and r(tk)
    for id, doc in coll.get_docs().items():
        if bench[id] > 0:
            for term, freq in doc.terms.items():
                try:
                    T[term] += 1 
                except KeyError:
                    T[term] = 1

    #calculate n(tk)
    ntk = {}
    for id, doc in coll.get_docs().items():

        for term, freq in doc.terms.items():
            try:
                ntk[term] += 1 
            except KeyError:
                ntk[term] = 1

    #calculate N and R
    no_docs = coll.get_num_docs()
    R = 0
    for id, freq in bench.items():
        if bench[id] > 0:
            R += 1

    P = {}
    for id, rtk in T.items():
        T[id] =math.log(((rtk+0.5) * (no_docs - ntk[id] - R + rtk + 0.5 )) / ((ntk[id] - rtk +0.5) * (R - rtk +0.5)))

    #calculate mean weight for all the documents
    mean_weight = 0
    for id, rtk in T.items():
        mean_weight += rtk
    if len(T) !=0:
        mean_weight = mean_weight / len(T)
    
    #Feature selection
    Features = {t: r for t, r in T.items() if r > mean_weight + theta}
    return Features


    '''main function to display and check the output'''

if __name__ == '__main__':

    i = 100
    while (i < 150):
        i = i + 1
        coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/DataCollection/Dataset" + str(i)  # to access the datasets # add your own path
        stopwords_f = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/common-english-words.txt', 'r') # add your own path
        stop_words = stopwords_f.read().split(',')
        stopwords_f.close()
        coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

        os.chdir('..')
        os.chdir('..')

        benchFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_benchmark/BM25_benchmark' + str(i) + '.txt')

        file_ = benchFile.readlines()

        bench = {}
        for line in file_:
            line = line.strip()
            lineList = line.split()
            bench[lineList[1]] = float(lineList[2])

        benchFile.close()
        theta = 3.5
        BM25_weights = BM25_Train(coll_, bench, theta)

        writeFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_features/BM25_features_R' + str(i) + '.dat', 'w') #add your path for the features
        for (k, v) in sorted(BM25_weights.items(), key=lambda x: x[1], reverse= True):
            writeFile.write(k + ' ' + str(v) + '\n')
        writeFile.close()





