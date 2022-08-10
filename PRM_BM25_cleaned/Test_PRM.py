# To test pseudo relevance model on the same data collection

# Function for calculating BM25 ranking score for all docs in data collection
def BM25Testing(coll, features):
    """
    Input: Collection folder as test set and features calculated in training script
    Output: Returns a dictionary of document as key and rank as value
    """
    ranks = {}
    for id, doc in coll.get_docs().items():
        Rank = 0
        for term in features.keys():
            if term in doc.get_term_list():
                try:
                    ranks[id] += features[term]
                except KeyError:
                    ranks[id] = features[term]
    return ranks


if __name__ == "__main__":
    import os
    import coll
    n = 10
    for i in range(101,151):
        coll_fname = "E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\DataCollection\Dataset" + str(i)  # to access the datasets # add your own path

        # pre-processing documents
        stopwords_f = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\common-english-words.txt', 'r')
        stop_words = stopwords_f.read().split(',')
        stopwords_f.close()
        coll_ = coll.parse_rcv_coll(coll_fname, stop_words)

        # get features
        os.chdir('..')
        os.chdir('..')
        featureFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\PRM_BM25_features\PModel_weight_R' + str(i) + '.dat')
        file_ = featureFile.readlines()
        features = {}
        for line in file_:
            line = line.strip()
            lineList = line.split()
            features[lineList[0]] = float(lineList[1])
        featureFile.close()

        # obtain ranks for all documents
        ranks = BM25Testing(coll_, features)

        wFile = open('E:\Downloads\Downloads\Ayush\PRM_BM25_cleaned\PRM_test_result\Test_ranks_PR' + str(i) + '.dat', 'w')
        for (d, v) in sorted(ranks.items(), key=lambda x: x[1], reverse=True):
            wFile.write(d + ' ' + '|' + ' ' + str(v) + '\n')
        wFile.close()

