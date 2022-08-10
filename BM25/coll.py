'''using the same code from assignemt 1 for creating class to docID, terms and docLen'''
import glob, os, string
from parso import parse
from stemming.porter2 import stem
class BowDoc:
    def __init__(self, docID):
        self.docID = docID
        self.terms = {}
        self.doc_len = 0

    def getDocId(self):
        return self.docID

    def addTerm(self, term):

        try:
            self.terms[term] += 1
        except KeyError:
            self.terms[term] = 1

    def getDocLen(self):
        return self.doc_len #accessor   
    
    def setDocLen(self, doc_len):
        self.doc_len = doc_len #mutator

    def term_list(self):
        return sorted(self.terms.keys())
    
    def term_freq(self):
        return self.terms

    def get_term_count(self, term):

        try:
            return self.terms[term]
        except KeyError:
            return 0 


class BowColl:

    def __init__(self):

        self.docs = {}
    
    def add_doc(self, doc):
        
        self.docs[doc.getDocId()] = doc

    def get_docs(self):

        return self.docs
    def get_num_docs(self):

        return len(self.docs)


'''using the assignment 1 code coll.py to calculate and store all the docids and objects'''
def parse_rcv_coll(inputpath, stop_words):

    coll = BowColl()
    os.chdir(inputpath) #the pathname of the directory that stores all the files.
    for file_ in glob.glob("*xml"):
        curr_doc = None
        start_end = False
        word_count = 0
        for line in open(file_):
            line = line.strip()
            if(start_end == False):
                if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            docid = part.split("=")[1].split("\"")[1]
                            curr_doc = BowDoc(docid)
                            break
                if line.startswith("<text>"):
                    start_end = True
            elif line.startswith("</text>"):
                break
            else:
                line = line.replace("<p>", "").replace("</p>", "")
                line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                line = line.replace("\\s+", " ")
                #print(line)

                for term in line.split():
                    word_count += 1
                    term = stem(term.lower())
                    if len(term) > 2 and term not in stop_words:
                        curr_doc.addTerm(term)
        if curr_doc is not None:
            curr_doc.setDocLen(word_count)
            coll.add_doc(curr_doc)
            #print(coll)
    return coll

'''main function to check and display the output of coll.py'''
if __name__ == '__main__':

    import sys, coll

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    stopwords = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/common-english-words.txt', 'r')
    stop_words = stopwords.read().split(',')
    stopwords.close()

    coll = parse_rcv_coll(sys.argv[1], stop_words)

    '''print function to display the output of the coll.py to check if the result is printing out correctly'''
    for id,doc in coll.get_docs().items():
        print('Doc ' + id + 'have ' + str(len(doc.term_list())) + ' terms and total' + str(doc.getDoclen()) + 'words')
        doc1 = doc.term_freq()
        doc2 = {k: v for k, v in sorted(doc1.items(), key=lambda item: item[1], reverse=True)}
        for term, freq in doc2.items():
            print(term + ' : ' + str(freq) + '\n')
        print('\n')