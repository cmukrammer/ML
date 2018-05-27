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

def _viterbiAlg(d):
    state = ['PR', 'VB', 'RB', 'NN', 'PC', 'JJ', 'DT', 'OT' ]
    l = len(hmmPrior)
    vp = [[float('-inf')]*(len(d)) for _ in range(l)]
    q = [[[] for _ in range(len(d))] for _ in range(l)]
    #print q
    for i in range(l):
        q[i][0] = [i]
    #print alpha
    for i in range(l):
        vp[i][0] = hmmPrior[i] + hmmEmit[i][d[0]]
    for t in range(1, len(d)):
        for i in range(l):
            argmax = 0
            for j in range(l):
                x = vp[j][t-1] + hmmTrain[j][i] + hmmEmit[i][d[t]]
                if x > vp[i][t]:
                    argmax = j
                    vp[i][t] = x
            q[i][t] = q[argmax][t-1] + [i]
    k = 0
    maxVP = float('-inf')
    for i in range(l):
        if vp[i][-1] > maxVP:
            k = i
            maxVP = vp[i][-1]
    for i in range(len(d)):
        d[i] += '_{}'.format(state[q[k][-1][i]])
    print ' '.join(d)

def viterbiAlg():
    for d in dev:
        _viterbiAlg(d)

def main(fn1, fn2, fn3, fn4):
    read_file(fn1, DEV)
    #print dev
    read_file(fn2, TRAIN)
    #print hmmTrain
    read_file(fn3, EMIT)
    #print hmmEmit
    read_file(fn4, PRIOR)
    #print hmmPrior
    viterbiAlg()

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print "Wrong argv number"
