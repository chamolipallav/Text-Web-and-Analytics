import glob, os, string, sys
from re import A

def Eval(inputpath, i, count):
    coll = {}

    A = {}
    B = {}
    R1 = {}
    R2 = {}

    for line in open("/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/BM25/RelevanceFeedback/Dataset" + str(i) + ".txt"):
        line = line.strip()
        lineList = line.split()
        A[lineList[1]] = int(float(lineList[2]))
    for line in open("/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_weight/IRM_Weight_R" + str(i) + ".dat"):
        line = line.strip()
        lineList = line.split()
        B[lineList[0]] = int(float(lineList[1]))
    return (A, B)

'''main fucntion to print the output and check  the fuction'''
if __name__ == "__main__":

    i = 101
    count = 1
    d = 0 
    precision = [0] * 51
    recall = [0] * 51
    F1 = [0] * 51
    precision[0] = 0.0
    temp_p = {}
    temp_r = {}
    temp_f1 = {}

    rank = {}
    j = 101

    temp_top = {}
    MeanRecall = 0
    MeanPrecision = 0
    MeanF1 = 0
    while i <= 150:
        (rel_doc, retrived_doc) = Eval(os.getcwd(), i, count)

        sortedBM25 = {k: v for k, v in sorted(rel_doc.items(), key=lambda item: item[1], reverse=True)}

        temp = {}
        for items1, keys1 in sortedBM25.items():
            temp.update({items1: 0})
            for items, keys in retrived_doc.items():
                if items == items1:

                    temp.update({items1: 1})
                    break
        
        R = 0
        for (x,y) in rel_doc.items():
            if (y == 1):
                R= R + 1

        R1 = 0
        for (x, y) in temp.items():
            if (y == 1):
                R1 = R1 + 1


        RR1 = 0 
        for (x, y) in rel_doc.items():
            if (y == 1) & (temp[x] == 1):
                RR1 = RR1 + 1

        r = float(RR1) / float(R)

        if R1 != 0:
            p = float(RR1) / float(R1)
        else:
            p = 0
        
        if p +r !=0:
            F1 = 2 * p * r / (p + r)

        else: 
            F1 = 0

        temp_p[count]= p
        temp_r[count] = r
        temp_f1[count] = F1

        temp_top[count] = i
        MeanRecall += r
        MeanPrecision += p
        MeanF1 += F1
        i = i +1
        count = count +1
        d = d +1

if count == 51:

    sortedprecision = {k: v for k, v in sorted(temp_p.items(), key=lambda item: item[1], reverse=True)} 
    sortedrecall = {k: v for k, v in sorted(temp_r.items(), key=lambda item: item[1], reverse=True)} 
    sortedF1 = {k: v for k, v in sorted(temp_f1.items(), key=lambda item: item[1], reverse=True)} 
    #sortedMap = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1], reverse=True)}

    k = 0
    g = 0
    writeFile = open("/Users/pallavchamoli/Downloads/IFN647/Assignment 2 IFN647/assignment deliverable/IMR_BM25/IRM_Result/Eval_Result.dat", 'w')
    writeFile.write('{:<6s}{:<25s}{:<25s}{:<25s}'.format("TOPIC", "PRECISION", "RECALL", "F1"))
    print('{:<6s}{:<25s}{:<25s}{:<25s}'.format("TOPIC", "PRECISION", "RECALL", "F1"))
    for i, j in sortedprecision.items():
        if (k < 51):
            k = k + 1
            writeFile.write('\n')
            writeFile.write('{:<6s}{:<25s}{:<25s}{:<25s}'.format(str(temp_top[i]), str(j), str(sortedrecall[i]),str(sortedF1[i])))

        if (g < 50):
            print('{:<6s}{:<25s}{:<25s}{:<25s}'.format(str(temp_top[i]), str(j), str(sortedrecall[i]),str(sortedF1[i])))
        
    print("Mean recall", MeanRecall / 50)
    print("Mean precision", MeanPrecision / 50)
    print("Mean F1", MeanF1 / 50)
    writeFile.close()