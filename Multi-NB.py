import numpy as np
import pandas as pd


V=[[]]
prior = 0.0
condProb = 0.0

C = [1,0]


def getprior_c(c,prior):
    for i in prior:
        if i[0] == c:
            return i[1]



def getCondProbwithCT(t, c, condProb):
    for i in condProb:
        if i[0] == t and i[1] == c:
            return i[2]


def ExtractVocabulary(D):
    RepVocwithd = []
    for d in D:
        voc_d = d[0].split()
        if voc_d not in RepVocwithd:
            RepVocwithd.append(voc_d)

    UniVoc = []
    for dv in RepVocwithd:
        for t in dv:
            if t not in UniVoc:
                UniVoc.append(t)

    return UniVoc

# print(ExtractVocabulary(D))


def CountDocsInClass(D,c):
    count = 0
    for d in D:
        if d[1]==c:
            count+=1
        
    return count

# print(CountDocsInClass(D,1))



def CountDocs(D):
    return len(D)


# print(CountDocs(D))

def ConcatenateTextOfAllDocsInClass(D,c):
    txt_concatenate = ""
    for d in D:
        if d[1]==c: # problem here  ....
            txt_concatenate = txt_concatenate + d[0] + " "
            
    return txt_concatenate

# print(ConcatenateTextOfAllDocsInClass(D,1))


def CountTokenOfTerms(concText,t):
    count = 0 
    lst = concText.split()
    for trm in lst:
        if trm == t:
            count += 1

    return count

def ExtractTokensFromDoc(V,d):
    return d.split()

# print(ExtractTokensFromDoc(ExtractVocabulary(D),'Chinese Chinese Japan Tokyo' ))


def TrainMultinomialNB(C,D):
    prior = []
    condProb = []
    
    
    V = ExtractVocabulary(D)
    N = CountDocs(D)
    for c in C:
        s_prior = []
        Nc = CountDocsInClass(D,c)
        prior_c = Nc/N
        s_prior.append(c)
        s_prior.append(prior_c)
        prior.append(s_prior)
        txtc = ConcatenateTextOfAllDocsInClass(D,c)
        for t in V:
            s_condProb = []
            Tct = CountTokenOfTerms(txtc, t)        
            condProb_c = (Tct + 1)/(len(txtc.split())+len(V)) 

            s_condProb.append(t)
            s_condProb.append(c)
            s_condProb.append(condProb_c)
        
            condProb.append(s_condProb)
        
    return V ,prior, condProb



# print(TrainMultinomialNB(C,D))


def ApplyMultinomialNB(C,V,prior,condProb,d):
    score = []
    l = []
    W = ExtractTokensFromDoc(V,d)
    for c in C:
        score_c = getprior_c(c,prior)
        for t in W:
            score_c = score_c * getCondProbwithCT(t, c, condProb)
        l.append(c)
        l.append(score_c)
        score.append(l)
        l = []


    if score[0][1]>score[1][1]:
        return 1
    else:
        return 0


def testClassifier(datafile, labelfile):
    traindata = pd.read_csv(datafile, header=None)
    trainlabels = pd.read_csv(labelfile, header = None)
    data = pd.concat([traindata, trainlabels], axis=1).reindex(traindata.index)
    traindatalist = data.values.tolist()

    V,prior,condProb = TrainMultinomialNB(C,traindatalist)
    CorrClassified = 0
    for d in traindatalist:
        d.append(ApplyMultinomialNB(C,V,prior,condProb,d[0]))
        if d[1] == d[2]:
            CorrClassified += 1

    acc = (CorrClassified * 100)/len(traindatalist)

    print(acc)


testClassifier('traindata.txt','trainlabels.txt')
testClassifier('testdata.txt','testlabels.txt')




