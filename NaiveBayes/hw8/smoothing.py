import sys
import math

V = {}
libDocN = 0
libWp = 0
conDocN = 0
conWp = 0
LIB = 0
CON = 1

def read_file(fn):
    with open(fn, 'r') as f:
        data = []
        for line in f:
            data.append(line[:-1].lower())
    return data

def buildV(train):
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    for fn in train:
        docSj = read_file(fn)
        if 'lib' in fn: 
            libDocN += 1
            libWp += len(docSj)
            for w in docSj:
                if w not in V:
                    V[w] = [0,0]
                V[w][LIB] += 1
        if 'con' in fn: 
            conDocN += 1
            conWp += len(docSj)
            for w in docSj:
                if w not in V:
                    V[w] = [0,0]
                V[w][CON] += 1

def logP(a, b):
    return math.log(float(a)/b)

def verifyTest(test, q):
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    #print libWp, conWp, len(V), libDocN, conDocN
    #print V
    #vlibw = 0
    #for w in V.keys():
    #    vlibw += V[w][0]
    #print vlibw
    pVLib = float(libDocN)/(libDocN+conDocN)
    pVCon = float(conDocN)/(libDocN+conDocN)
    #print pVLib, pVCon
    vSize = len(V)
    allTest = 0
    right = 0
    for f in test:
        words = read_file(f)
        pNBLib = logP(pVLib, 1)
        #print "pNBLib", pNBLib
        for w in words:
            nk = 0
            if w in V:
                nk = V[w][LIB]
                pNBLib += logP((nk+q), (libWp+q*vSize))
            #print "pNBLib", w, w in V, pNBLib
        pNBCon = logP(pVCon, 1)
        #print "pNBCon", pNBCon
        for w in words:
            nk = 0
            if w in V:
                nk = V[w][CON]
                pNBCon += logP((nk+q), (conWp+q*vSize))
            #print "pNBCon", w, w in V, pNBCon
        allTest += 1
        if pNBLib > pNBCon:
            if 'lib' in f:
                right += 1
            print 'L'#, pNBLib, pNBCon
        elif pNBCon > pNBLib:
            if 'con' in f:
                right += 1
            print 'C'#, pNBLib, pNBCon
    print 'Accuracy: {0:.4f}'.format(float(right)/allTest)

def main(fn1, fn2, q):
    train = read_file(fn1)
    #print train
    buildV(train)
    #print V
    #print len(V)
    test = read_file(fn2)
    verifyTest(test, float(q))

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Wrong argv number"
