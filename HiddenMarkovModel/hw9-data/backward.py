import sys
import math
from logsum import log_sum

DEV = 0
TRAIN = 1
EMIT = 2
PRIOR = 3

dev = []
hmmTrain = []
hmmEmit = []
hmmPrior = []

def log(x):
    if not isinstance(x, float):
        x = float(x)
    return math.log(x)

def read_file(fn, case):
    with open(fn, 'r') as f:
        for line in f:
            if case == DEV:
                dev.append(line[:-1].split(" "))
            if case == TRAIN:
                l = [ log(x.split(':')[1]) for x in line[:-1].split(" ") if ':' in x]
                hmmTrain.append(l)
            if case == EMIT:
                r = []
                for x in line[:-1].split(" "):
                    if ':' in x:
                        y = x.split(':')
                        y[1] = log(y[1])
                        r.append(y)
                hmmEmit.append(dict(r))
            if case == PRIOR:
                hmmPrior.append(log(line[:-1].split(' ')[1]))

def _backwardAlg(d):
    l = len(hmmPrior)
    beta = [[0]*(len(d)) for _ in range(l)]
    #print alpha
    #for i in range(l):
    #    beta[i][-1] = 1
    for t in range(len(d)-2, -1, -1):
        for i in range(l):
            #print t, i, d[t], hmmEmit[i][d[t]], alpha[t][i]
            x = beta[0][t+1] + hmmTrain[i][0] + hmmEmit[0][d[t+1]]
            for j in range(1, l):
                x = log_sum(x, beta[j][t+1] + hmmTrain[i][j] + hmmEmit[j][d[t+1]])
            beta[i][t] = x
    #print alpha
    x = beta[0][0] + hmmPrior[0] + hmmEmit[0][d[0]]
    for i in range(1, l):
        x = log_sum(x, beta[i][0] + hmmPrior[i] + hmmEmit[i][d[0]])
    print x

def backwardAlg():
    for d in dev:
        _backwardAlg(d)

def main(fn1, fn2, fn3, fn4):
    read_file(fn1, DEV)
    #print dev
    read_file(fn2, TRAIN)
    #print hmmTrain
    read_file(fn3, EMIT)
    #print hmmEmit
    read_file(fn4, PRIOR)
    #print hmmPrior
    backwardAlg()

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print "Wrong argv number"
