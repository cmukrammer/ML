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

def topWords():
    global V, libDocN, libWp, conDocN, conWp, LIB, CON
    vSize = len(V)
    topLib = []
    topCon = []
    for w in V.keys():
        pWLib = float(V[w][LIB]+1)/(libWp+vSize)
        pWCon = float(V[w][CON]+1)/(conWp+vSize)
        heapq.heappush(topLib, (pWLib, w))
        heapq.heappush(topCon, (pWCon, w))
        if len(topLib) > 20: heapq.heappop(topLib)
        if len(topCon) > 20: heapq.heappop(topCon)
    topLib.sort(key=lambda x: x[0], reverse=True)
    topCon.sort(key=lambda x: x[0], reverse=True)
    for w in topLib:
        print '{} {:.04f}'.format(w[1], w[0])
    print ''
    for w in topCon:
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
