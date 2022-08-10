'''Train model is just an extra feature to improve the result for IRM model. this is not compulsory'''
import math
from stemming.porter2 import stem
import sys, os, coll, df

def avg_doc_len(coll):
    tot_dl = 0
    for id, doc in coll.get_docs().items():
        tot_dl = tot_dl + doc.get_doc_len()
    return tot_dl/coll.get_num_docs()
    
def IRM_Train(coll, ben, theta):
    T={}
    # select T from positive documents and r(tk)
    for id, doc in coll.get_docs().items():
        if ben[id] > 0:
            for term, freq in doc.terms.items():
                try:
                    T[term] += 1
                except KeyError:
                    T[term] = 1
    #calculate n(tk)
    ntk = {}
    for id, doc in coll.get_docs().items():
        for term in doc.get_term_list():
            try:
                ntk[term] += 1
            except KeyError:
                ntk[term] = 1
    
    #calculate N and R
                    
    No_docs = coll.get_num_docs()
    R = 0
    for id, fre in ben.items():
        if ben[id] > 0:
            R += 1
    
    for id, rtk in T.items():
        T[id] = ((rtk+0.5) / (R-rtk + 0.5)) / ((ntk[id]-rtk+0.5)/(No_docs-ntk[id]-R+rtk +0.5)) 

    #calculate the mean of w4 weights.
    meanW5= 0
    for id, rtk in T.items():
        meanW5 += rtk
    if len(T) !=0:
        meanW5 = meanW5 / len(T)
    

    #Features selection
    Features = {t:r for t,r in T.items() if r > meanW5 + theta }
    return Features
if __name__ == '__main__':

    i = 100
    while (i < 150):
        i = i + 1
        coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/DataCollection/Dataset" + str(i)  # to access the datasets # add your own path
        stopwords_f = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/common-english-words.txt', 'r') # add your own path
        stop_words = stopwords_f.read().split(',')
        stopwords_f.close()
        coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

        os.chdir('..')
        os.chdir('..')

        benchFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_benchmark/IRM_benchmark' + str(i) + '.txt')

        file_ = benchFile.readlines()

        bench = {}
        for line in file_:
            line = line.strip()
            lineList = line.split()
            bench[lineList[1]] = float(lineList[2])

        benchFile.close()
        theta = 3.5
        BM25_weights = IRM_Train(coll_, bench, theta)

        writeFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_features/IRM_features_R' + str(i) + '.dat', 'w') #add your path for the features
        for (k, v) in sorted(BM25_weights.items(), key=lambda x: x[1], reverse= True):
            writeFile.write(k + ' ' + str(v) + '\n')
        writeFile.close()