import math
from stemming.porter2 import stem
import sys, os, coll, df

def avg_doc_len(coll):
    tot_dl = 0
    for id, doc in coll.get_docs().items():
        tot_dl = tot_dl + doc.get_doc_len()
    return tot_dl/coll.get_num_docs()

# Task 2 - BM25 based IR model

def bm25(coll, q, df):
    bm25s = {}
    avg_dl = avg_doc_len(coll)
    no_docs = coll.get_num_docs()
    for id, doc in coll.get_docs().items():
        query_terms = q.split()
        qfs = {}        
        for t in query_terms:
            term = stem(t.lower())
            try:
                qfs[term] += 1
            except KeyError:
                qfs[term] = 1
        k = 1.2 * ((1 - 0.75) + 0.75 * (doc.get_doc_len() / float(avg_dl)))
        bm25_ = 0.0
        for qt in qfs.keys():
            n = 0
            if qt in df.keys():
                n = df[qt]
                f = doc.get_term_count(qt)
                qf = qfs[qt]
                bm = math.log(1.0 / ((n + 0.5) / (no_docs - n + 0.5)), 2) * (((1.2 + 1) * f) / (k + f)) * ( ((100 + 1) * qf) / float(100 + qf))
                # bm valuse may be negative if no_docs < 2n+1, so we may use 3*no_docs to solve this problem.
                bm25_ += bm
        bm25s[doc.get_docid()] = bm25_
    return bm25s


if __name__ == "__main__":

    dataset_doc = ""
    query = ""

    inputText = open('Topics.txt', 'r') # add your own path of topics.txt
    top = 0
    flag = 0
    for line in inputText.readlines():
        if flag != 1:
            if line.startswith("<top>"):
                query = ""
                top = 1
            if line.startswith("<num>"):
                dataset_doc = line[15:]
                dataset_doc = dataset_doc[:3]
            elif line.startswith("</top>"):
                flag = 0 
            else:
                if line.startswith("<title>"):
                    query = line[7:]
                    flag = 1

        if flag == 1:
            flag = 0
            coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/DataCollection/Dataset" + dataset_doc  # to access the datasets # add your own path

            # it would be better to have a class that represents the index and stores DF dictionary\

            stopwords = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/common-english-words.txt', 'r')# add your own path
            stop_words = stopwords.read().split(',')
            stopwords.close()
            coll_ = coll.parse_rcv_coll(coll_fname, stop_words)
            df_ = df.calc_df(coll_)
            bm25_ = bm25(coll_, query, df_)
            print('QUERY: ' + " " + query + " \n") # displaying all the titles as Q = Query

            os.chdir('..') # changing directory
            os.chdir('..')

            '''storing all the weight data in BM25_weight'''
            #os.chdir('.\BM25_weight')

            wFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_weight/IRM_Weight_R' + dataset_doc + '.dat', 'a') # add your own path

            for (k, v) in sorted(bm25_.items(), key=lambda x: x[1], reverse=True):
                wFile.write(k + ' ' + str(v) + '\n')

            wFile.close()
            '''storing all the output for topics 101-150 in BM25_benchmark'''
            #os.chdir('..')
            #os.chdir('.\BM25_benchmark')

            wFile_1 = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_benchmark/IRM_benchmark' + dataset_doc + '.txt', 'a')# add your own path

            dataFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_weight/IRM_Weight_R' + dataset_doc + '.dat')# add your own path
            file_ = dataFile.readlines()
            for line in file_:
                line = line.strip()
                lineStr = line.split()
                if float(lineStr[1]) > 1:  #Significance of > 1

                    wFile_1.write('R' + dataset_doc + " " + lineStr[0] + ' 1' + '\n')

                else:
                    wFile_1.write('R' + dataset_doc + " " + lineStr[0] + ' 0' + '\n')

            wFile_1.close()
            dataFile.close()