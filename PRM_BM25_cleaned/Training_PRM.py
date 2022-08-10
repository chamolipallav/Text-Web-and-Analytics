# It uses Data collection and PTraining_benchmark.txt

# to calculate the average document length
def avg_doc_len(coll):
    """
    Input: Data collection
    Return: Average Document length
    """
    tot_dl = 0
    for id, doc in coll.get_docs().items():
        tot_dl = tot_dl + doc.get_doc_len()
    return tot_dl / coll.get_num_docs()


# To evaluate the term weight
def w5(coll, ben, theta):
    """
    Input: Data collection, training benchmark file, experimental parameter (Theta)
    Output: A dictionary of features with their weights
    """
    T = {}
    # select T from positive documents and r(tk)
    for id, doc in coll.get_docs().items():
        if ben[id] > 0:
            for term, freq in doc.terms.items():
                try:
                    T[term] += 1
                except KeyError:
                    T[term] = 1

    # calculate n(tk)
    ntk = {}
    for id, doc in coll.get_docs().items():
        for term in doc.get_term_list():
            try:
                ntk[term] += 1
            except KeyError:
                ntk[term] = 1

    # calculate N and R
    No_docs = coll.get_num_docs()
    R = 0
    for id, fre in ben.items():
        if ben[id] > 0:
            R += 1

    for id, rtk in T.items():
        T[id] = ((rtk + 0.5) / (R - rtk + 0.5)) / ((ntk[id] - rtk + 0.5) / (No_docs - ntk[id] - R + rtk + 0.5))

    # calculate the mean of w5 weights.
    meanW5 = 0
    for id, rtk in T.items():
        if len(T) != 0:
            meanW5 += rtk
        else:
            meanW5 = 0
        meanW5 = meanW5 / len(T)

        meanW5 = meanW5 / len(T)

    # Features selection
    Features = {t: r for t, r in T.items() if r > meanW5 + theta}
    return Features


if __name__ == "__main__":
    import os
    import coll

    i = 100
    while (i < 150):
        i = i + 1
        # to access the datasets add your own path
        # use data collection as an input argument
        coll_fname = "E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\DataCollection\Dataset" + str(i)
        stopwords_f = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\common-english-words.txt', 'r')
        stop_words = stopwords_f.read().split(',')
        stopwords_f.close()

        # use document parsing to represent training set
        coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

        os.chdir('..')
        os.chdir('..')

        # the pesudo relevance judgements
        benFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\Ptraining_benchmark\Ptraining_benchmark_' + str(i) + '.txt')
        file_ = benFile.readlines()

        ben = {}
        for line in file_:
            line = line.strip()
            lineList = line.split()
            ben[lineList[1]] = float(lineList[2])

        benFile.close()
        theta = 3.5
        bm25_weights = w5(coll_, ben, theta)

        # add your path for the features
        wFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\PRM_BM25_features\PModel_weight_R' + str(i) + '.dat', 'w')
        for (k, v) in sorted(bm25_weights.items(), key=lambda x: x[1], reverse=True):
            wFile.write(k + ' ' + str(v) + '\n')
        wFile.close()
