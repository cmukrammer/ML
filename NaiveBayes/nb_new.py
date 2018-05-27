import sys
import math

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
        if type.find('con'): #'con'
            data.append(0)
        else:
            data.append(1)
        dataSet.append(data)
    return dataSet


def getVocab(dataSet):
    vocab = set([])
    for data in dataSet:
        l = data[0]
        vocab = vocab | set(l)
    return list(vocab)

def train(dataSet, vocab):
    numC, numL = 0.0, 0.0
    wordC, wordL = {},{}
    for data in dataSet:
        if data[1] == 0:
            print '1st if data[1]=', data[1]
            for i in range(10):
                print data[0][i]
            numC += 1
            for word in data[0]:
                wordC[word] = wordC.get(word, 0) + 1
        else:
            print 'data[1]=', data[1]
            for i in range(10):
                print data[0][i]
            numL += 1
            for word in data[0]:
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
    for data in dataSetTest:
        num += 1
        pc = math.log(ph0)
        pl = math.log(ph1)
        for word in data[0]:
            pc += math.log(pC.get(word,1))
            pl += math.log(pL.get(word,1))
        #print 'c', pc, 'l', pl
        if pc > pl:
            #result.append('C')
            result.append('L')
            if data[1] == 0:
                #print 'd1', data[1],'d',data[0]
                correct += 1
        else:
            #result.append('L')
            result.append('C')
            if data[1] == 1:
                correct += 1
    return result, correct/num


def main():
    files = sys.argv[1:]
    dataSetTrain = getData(files[0])
    dataSetTest = getData(files[1])
    vocab = getVocab(dataSetTrain)
    pC, pL, ph0, ph1 = train(dataSetTrain,vocab)
   # for word in pC:
        #print '1',pC[word]
      #  pC[word] = math.log(pC[word])
      #  print '2', pC[word]
    #print 'pc',pC
    #print 'pl',pL
    result, rate = classify(dataSetTest,vocab,pC, pL, ph0, ph1)
    for i in result:
        print i
    print 'Accuracy: %.04f'%(rate)


if __name__ == '__main__':
    main()
