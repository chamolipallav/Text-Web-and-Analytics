import math
from stemming.porter2 import stem

# for calculating average document length
def avg_doc_len(coll):
    tot_dl = 0
    for id, doc in coll.get_docs().items():
        tot_dl = tot_dl + doc.get_doc_len()
    return tot_dl / coll.get_num_docs()

# for calculating the weight of each document based on query
def bm25(coll, q, df):
    """
    Input: Data collection, Query and Data frequency
    Return: A dictionary of doc_ID as key and score as value
    """
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
                bm = math.log(1.0 / ((n + 0.5) / (no_docs - n + 0.5)), 2) * (((1.2 + 1) * f) / (k + f)) * (
                            ((100 + 1) * qf) / float(100 + qf))
                # bm value may be negative if no_docs < 2n+1, so we may use 3*no_docs to solve this problem.
                bm25_ += bm
        bm25s[doc.get_docid()] = bm25_
    return bm25s


if __name__ == "__main__":
    import os
    import coll
    import df

    # import query
    dataset_doc = ""
    query = ""

    # extract query and dataset ID from Topic
    inputText = open('Topics.txt', 'r')  # add your own path of topics.txt
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
            coll_fname = "E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\DataCollection\Dataset" + dataset_doc  # to access the datasets add your own path
            stopwords_f = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\common-english-words.txt', 'r')
            stop_words = stopwords_f.read().split(',')
            stopwords_f.close()

            # document parsing
            coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

            # calculate document frequency
            df_ = df.calc_df(coll_)

            # call bm25_ to calculate the BM25 score for all the documents in the given Data Collection
            bm25_1 = bm25(coll_, query, df_)

            print('For query Q = ' + query)

            os.chdir('..')  # changing directory
            os.chdir('..')

            # sorting all the docs according to high - low BM25 score and save the file in .dat format
            wFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\PRM_BM25_weight\WeightSum_R' + dataset_doc + '.dat', 'a') # add your own path
            for (k, v) in sorted(bm25_1.items(), key=lambda x: x[1], reverse=True):
                wFile.write(k + ' ' + str(v) + '\n')
            wFile.close()

            # creating benchmark file to be used as input while training the model
            writeFile = open("E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\Ptraining_benchmark\Ptraining_benchmark_" + dataset_doc + ".txt", 'a')
            bm25_threshold = 1.0

            # based on sorted doc - BM25 score doing the information filtering for relevance docs
            dataFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\PRM_BM25_weight\WeightSum_R' + dataset_doc + '.dat')  # add your own path
            file_ = dataFile.readlines()
            for line in file_:
                line = line.strip()
                lineStr = line.split()
                if float(lineStr[1]) > bm25_threshold:
                    writeFile.write('R' + dataset_doc + " " + lineStr[0] + ' 1' + '\n')
                else:
                    writeFile.write('R' + dataset_doc + " " + lineStr[0] + ' 0' + '\n')
            writeFile.close()
            dataFile.close()
