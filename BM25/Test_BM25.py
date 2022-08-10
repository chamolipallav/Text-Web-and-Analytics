from cProfile import label
import math
from stemming.porter2 import stem
import sys, os, coll, df

#Ranking docuemnt for BM25
def BM25_Test(coll, features):
    rank = {}
    for id, doc in coll.get_docs().items():
        for term in features.keys():
            if term in doc.term_list():
                try:
                    rank[id] += features[term]
                except KeyError:
                    rank[id] = features[term]
    return rank

'''defining main function to check out and display error'''

if __name__ == "__main__":

    i = 101
    count = 1
    while i <=150:
        coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/DataCollection/Dataset" + str(i)  # to access the datasets # add your own path
        stopwords_f = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/common-english-words.txt', 'r') # add your own path
        stop_words = stopwords_f.read().split(',')
        stopwords_f.close()
        coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

        # changing directory to access the other data
        os.chdir('..')
        os.chdir('..')

        # retrieve all the positive features
        featureFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_features/BM25_features_R' + str(i) + '.dat')
        file_ = featureFile.readlines()
        features = {}
        for line in file_:
            line = line.strip()
            lineList = line.split()
            features[lineList[0]] = float(lineList[1])
        featureFile.close()

        #obtain ranks for all the documents
        rank = BM25_Test(coll_, features)

        writeFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_results/result_R' + str(count) + '.dat', 'w') #add your own path
        for (d, v) in sorted(rank.items(), key=lambda x: x[1], reverse = True):
            writeFile.write(d + ' ' + '1' + ' ' + str(v) + '\n')
        writeFile.close()

        i = i + 1
        count = count + 1
        '''
        k = 101
    benFile =  open("/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/RelevanceFeedback/Dataset" + str(k) + ".txt")
    file_ = benFile.readline()
    ben = {}
    for line in file_:
        line = line.strip()
        lineList = line.split()
        ben[lineList[1]] = float(lineList[2])
        k = k + 1
    benFile.close()

    for line in open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_results/result_R' + str(k) + '.dat'):
        line = line.strip()
        lineList =  line.split()
        rank[str(j)] = lineList[0]
        j = j + 1

    ri = 0
    map = 0.0
    R = len([id for (id,v) in ben.items() if v>0 ])
    for (n, id) in sorted(rank.items(), key=lambda x: int(x[0])):
        if (ben[id] > 0):
            ri = ri + 1
            pi = float(ri)/ float(int(n))
            recall = float(ri)/ float(R)
            map = map + pi
    map = map/float(ri)

    print("average precision = " + str(map))


'''
