import sys
import math

vocab = []

def getData(file):
    dataSet = []
    fopen = open(file, 'r')
    types = fopen.readlines()
    fopen.close()
    for type in types:
        data = []
        type = type.strip()
        fopen = open(type, 'r')
        lines = fopen.readlines()
        fopen.close()
        l = []
        for line in lines:
            line = line.strip().lower()
            l.append(line)
        data.append(l)
        if 'con' in type:  # 'con'
            data.append(0)
        if 'lib' in type:
            data.append(1)
        dataSet.append(data)
    return dataSet


def getVocab(dataSet, N):
    vocab = {}
    lib, con = {}, {}
    for data in dataSet:
        if data[1] == 0: #con
            for word in data[0]:
                con[word] = con.get(word,0)+1
        if data[1] == 1:
            for word in data[0]:
                lib[word] = lib.get(word,0)+1
    con = sorted(con.iteritems(), key=lambda item: item[1], reverse=True)
    #print con[:N]
    lib = sorted(lib.iteritems(), key=lambda item: item[1], reverse=True)
    #print lib[:N]
    con = [ x[0] for x in con[:N]]
    lib = [ x[0] for x in lib[:N]]
    #print con
    for data in dataSet:
        for word in data[0]:
            if word in con or word in lib: continue
            vocab[word] = vocab.get(word,0)+1
    #if 'are' in vocab:
    #    print 'are in vocab'
    #print vocab
    return list(vocab), con, lib

def train(dataSet, vocab, stopCon, stopLib):
    numC, numL = 0.0, 0.0
    wordC, wordL = {},{}
    for data in dataSet:
        if data[1] == 0:
            numC += 1
            for word in data[0]:
                if word in stopCon or word in stopLib: continue
                wordC[word] = wordC.get(word, 0) + 1
        else:
            numL += 1
            for word in data[0]:
                if word in stopCon or word in stopLib: continue
                wordL[word] = wordL.get(word, 0) + 1
    ph0 = numC / (numC + numL)
    ph1 = numL / (numC + numL)
    numWordC = float(sum(wordC.values()))
    numWordL = float(sum(wordL.values()))
    pC = {}
    pL = {}
    for word in vocab:
        nk1 = wordC.get(word, 0)
        nk2 = wordL.get(word, 0)
        p0 = (nk1 + 1.0)/(numWordC + len(vocab))
        p1 = (nk2 + 1.0)/(numWordL + len(vocab))
        pC.setdefault(word,p0)
        pL.setdefault(word,p1)
    return pC, pL, ph0, ph1

def classify(dataSetTest, vocab, pC, pL, ph0, ph1):
    result = []
    num, correct = 0.0, 0.0
    #print len(vocab)
    #newV = [ x[0] for x in vocab ]
    #print newV
    for data in dataSetTest:
        num += 1
        pc = math.log(ph0)
        pl = math.log(ph1)
        for word in data[0]:
            #if word in vocab:
            pc += math.log(pC.get(word,1))
            pl += math.log(pL.get(word,1))
        if pc > pl:
            result.append('C')
            if data[1] == 0:
                #print 'd1', data[1],'d',data[0]
                correct += 1
        else:
            result.append('L')
            if data[1] == 1:
                correct += 1
    return result, correct/num


def main():
    global vocab
    files = sys.argv[1:]
    dataSetTrain = getData(files[0])
    dataSetTest = getData(files[1])
    N = int(files[2])
    vocab, stopCon, stopLib = getVocab(dataSetTrain, N)
    pC, pL, ph0, ph1 = train(dataSetTrain,vocab, stopCon, stopLib)
    result, rate = classify(dataSetTest,vocab,pC, pL, ph0, ph1)
    for i in result:
        print i
    print 'Accuracy: %.04f'%(rate)


if __name__ == '__main__':
    main()
