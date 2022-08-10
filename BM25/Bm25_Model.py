import math
from stemming.porter2 import stem
from datetime import datetime
import sys, os, coll, df


''' we are going to calculate average documne length for bm25 '''

def avg_doc_len(coll):
    total_dl = 0
    for id, doc in coll.get_docs().items():
        total_dl = total_dl + doc.getDocLen()
    return total_dl / coll.get_num_docs()

''' defining the fuction and algorithm for BM25. to make it generic we have recall the same methods we have done in assignment 1 '''
def BM25(coll, q, df):
    bm25_dic = {}
    avg_dl = avg_doc_len(coll)
    no_doc = coll.get_num_docs()
    for id, doc in coll.get_docs().items():
        query_terms = q.split()
        qfs = {}

        for t in query_terms:
            term = stem(t.lower())
            try:
                qfs[term] +=1
            except KeyError:
                qfs[term] = 1
        
        '''calculation k for BM25'''
        k = 1.2 * ((1 - 0.75)+ 0.75 * (doc.getDocLen() / float(avg_dl)))
        #print(doc.getDocLen())
        #print(avg_dl)
        bm25_ = 0.0
        for qt in qfs.keys():
            n = 0
            if qt in df.keys():
                n = df[qt]
                f = doc.get_term_count(qt)
                delta = 1
                
                '''calculate bm25 using the equation'''

                bm = math.log(1.0 / ((n)/ (no_doc+1)), 2) * ((((1.2 + 1) * f) / (k + f)) + delta)
                bm25_ += bm
            bm25_dic[doc.getDocId()] = bm25_
    return bm25_dic
    


'''defining main section with all the necessary execution process and process'''

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
            coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/DataCollection/Dataset" + dataset_doc  # to access the datasets # add your own path

            # it would be better to have a class that represents the index and stores DF dictionary\

            stopwords = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/common-english-words.txt', 'r')# add your own path
            stop_words = stopwords.read().split(',')
            stopwords.close()
            coll_ = coll.parse_rcv_coll(coll_fname, stop_words)
            df_ = df.calc_df(coll_)
            bm25_ = BM25(coll_, query, df_)
            print('QUERY: ' + " " + query + " \n") # displaying all the titles as Q = Query

            os.chdir('..') # changing directory
            os.chdir('..')

            '''storing all the weight data in BM25_weight'''
            #os.chdir('.\BM25_weight')

            wFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_weight/WeightSum_R' + dataset_doc + '.dat', 'a') # add your own path

            for (k, v) in sorted(bm25_.items(), key=lambda x: x[1], reverse=True):
                wFile.write(k + ' ' + str(v) + '\n')

            wFile.close()
            '''storing all the output for topics 101-150 in BM25_benchmark'''
            #os.chdir('..')
            #os.chdir('.\BM25_benchmark')

            wFile_1 = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_benchmark/BM25_benchmark' + dataset_doc + '.txt', 'a')# add your own path

            dataFile = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/BM25_weight/WeightSum_R' + dataset_doc + '.dat')# add your own path
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










