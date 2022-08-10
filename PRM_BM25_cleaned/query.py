import sys
import os
import coll
import df

def Query():
    dataset_doc = ""
    query = ""

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
            coll_fname = "/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/Assignment_2_Ayush/DataCollection/Dataset" + dataset_doc  # to access the datasets # add your own path

            # it would be better to have a class that represents the index and stores DF dictionary\


print(Query())