'''using the same code from assignment 1 to calculate the document frequency for each term and return as term: df dicitonary'''
def calc_df(coll):
    df_ = {}
    for id, doc in coll.get_docs().items():
        for term in doc.term_list():
            try:
                df_[term] += 1
            except KeyError:
                df_[term] = 1

    return df_

'''main function to run and display the output of document frequency '''
if __name__ == '__main__':

    import sys, coll

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    stopwords = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/common-english-words.txt', 'r') # add your own path
    stop_words = stopwords.read().split(',')
    stopwords.close()

    #calling coll.py to return objects 
    coll_ = coll.parse_rcv_coll(sys.argv[1], stop_words)
    df_ = calc_df(coll_)

    '''print function to display the output of the df.py to check if the result is printing out correctly'''
    print('There are ' +str(coll.get_num_docs()) + 'doc in dataset and contains '+ str(len(df_))+ 'terms')
    for (term, df_) in iter(sorted(df_.items(), key=lambda x: x[1],reverse=True)):
        print(term + ' : '+ str(df_))