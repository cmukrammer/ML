import sys
import math
import heapq

V = {}
libDocN = 0
libWp = 0
conDocN = 0
conWp = 0
LIB = 0
CON = 1
libStopW = {}
conStopW = {}

def read_file(fn):
    with open(fn, 'r') as f:
        data = []
        for line in f:
            data.append(line[:-1].lower())
    return data

def buildV(train, topList):
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    if topList:
        V = {}
        libDocN, libWp, conDocN, conWp = 0, 0, 0, 0
        #print libStopW, conStopW
    for fn in train:
        docSj = read_file(fn)
        if 'lib' in fn: 
            libDocN += 1
            for w in docSj:
                if topList and (w in libStopW or w in conStopW): continue
                libWp += 1
                if w not in V:
                    V[w] = [0,0]
                V[w][LIB] += 1
        if 'con' in fn: 
            conDocN += 1
            for w in docSj:
                if topList and (w in conStopW or w in libStopW): continue
                conWp += 1
                if w not in V:
                    V[w] = [0,0]
                V[w][CON] += 1

def topWords(n):
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    vSize = len(V)
    topLib = []
    topCon = []
    for w in V.keys():
        pWLib = float(V[w][LIB]+1)/(libWp+vSize)
        pWCon = float(V[w][CON]+1)/(conWp+vSize)
        heapq.heappush(topLib, (pWLib, w))
        heapq.heappush(topCon, (pWCon, w))
        if len(topLib) > n: heapq.heappop(topLib)
        if len(topCon) > n: heapq.heappop(topCon)
    topLib.sort(key=lambda x: x[0], reverse=True)
    topCon.sort(key=lambda x: x[0], reverse=True)
    for w in topLib:
        #print w[1], w[0]
        libStopW[w[1]] = 1
    #print ''
    for w in topCon:
        #print w[1], w[0]
        conStopW[w[1]] = 1
    #print 'same words rate: ', float(len(set(libStopW.keys())&set(conStopW.keys())))/n

def verifyTest(test):
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    print len(V)
    #print libWp, conWp
    pVLib = float(libDocN)/(libDocN+conDocN)
    pVCon = float(conDocN)/(libDocN+conDocN)
    vSize = len(V)
    allTest = 0
    right = 0
    for f in test:
        words = read_file(f)
        pNBLib = math.log(pVLib)
        for w in words:
            nk = 0
            if w in V:
                nk = V[w][LIB]
                pNBLib += math.log(float(nk+1)/(libWp+vSize))
        pNBCon = math.log(pVCon)
        for w in words:
            nk = 0
            if w in V:
                nk = V[w][CON]
                pNBCon += math.log(float(nk+1)/(conWp+vSize))
        allTest += 1
        if pNBLib > pNBCon:
            if 'lib' in f:
                right += 1
            print 'L'#, pNBLib, pNBCon
        elif pNBCon > pNBLib:
            if 'con' in f:
                right += 1
            print 'C'#, pNBLib, pNBCon
    print 'Accuracy: {:.4f}'.format(float(right)/allTest)

def main(fn1, fn2, n):
    train = read_file(fn1)
    #print train
    buildV(train, 0)
    topWords(int(n))
    buildV(train, 1)
    #print V
    #print len(V)
    test = read_file(fn2)
    verifyTest(test)



if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Wrong argv number"
