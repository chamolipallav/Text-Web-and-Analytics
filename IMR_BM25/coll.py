import glob, os
import string
from typing import KeysView
from stemming.porter2 import stem

class BowDoc:
    def __init__(self, docid):

        self.docid = docid
        self.terms = {}
        self.doc_len = 0 

    def add_term(self, term):

        try:
            self.terms[term] += 1
        except KeyError:
            self.terms[term] = 1

    def get_term_count(self, term):

        try:
            return self.terms[term]
        except KeyError:
            return 0 

    def get_term_freq_dict(self):
        
        return self.terms
    def get_term_list(self):
        return sorted(self.terms.keys())

    def get_docid(self):
        return self.docid
    
    def __iter__(self):

        return iter(sorted(self.terms.items(), key=lambda x: x[1], reverse=True))

    def get_doc_len(self):
        return self.doc_len

    def set_doc_len(self, doc_len):
        self.doc_len = doc_len

class BowColl:
    def __init__(self):

        self.docs = {}

    def add_doc(self, doc):
        self.docs[doc.get_docid()] = doc

    def get_doc(self, docid):
        return self.docs[docid]
    
    def get_docs(self):

        return self.docs

    def inorder_iter(self):

        return BowCollInorderIterator(self)

    def get_num_docs(self):
        return len(self.docs)

    def __iter__(self):

        return self.inorder_iter()

class BowCollInorderIterator:
    def __init__(self, coll):

        self.coll =coll
        self.keys = sorted(coll.get_docs().keys())
        self.i = 0

    def __iter__(self):

        return self
    
    def next(self):
        if self.i >= len(self.Keys):
            raise StopIteration
        doc = self.coll.get_doc(self.keys[self.i])
        self.i += 1
        return doc

def parse_rcv_coll(inputpath, stop_words):

    coll = BowColl()
    os.chdir(inputpath) 
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
                        curr_doc.add_term(term)
        if curr_doc is not None:
            curr_doc.set_doc_len(word_count)
            coll.add_doc(curr_doc)
            #print(coll)
    return coll

if __name__ == '__main__':

    import sys, coll

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    stopwords = open('/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/common-english-words.txt', 'r') # replace with your path for common english file
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
