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

def topWords():
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    vSize = len(V)
    topLibToCon = []
    topConToLib = []
    for w in V.keys():
        pWLib = float(V[w][LIB]+1)/(libWp+vSize)
        pWCon = float(V[w][CON]+1)/(conWp+vSize)
        heapq.heappush(topLibToCon, (logP(pWLib, pWCon), w))
        heapq.heappush(topConToLib, (logP(pWCon, pWLib), w))
        if len(topLibToCon) > 20: heapq.heappop(topLibToCon)
        if len(topConToLib) > 20: heapq.heappop(topConToLib)
    topLibToCon.sort(key=lambda x: x[0], reverse=True)
    topConToLib.sort(key=lambda x: x[0], reverse=True)
    for w in topLibToCon:
        print '{} {:.04f}'.format(w[1], w[0])
    print ''
    for w in topConToLib:
        print '{} {:.04f}'.format(w[1], w[0])

def main(fn1):
    train = read_file(fn1)
    #print train
    buildV(train)
    #print V
    #print len(V)
    topWords()



if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Wrong argv number"
