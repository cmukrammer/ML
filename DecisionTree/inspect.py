import sys
import csv
import math

def Entropy(data):
    inp = [ float(data.count(x))/len(data) for x in set(data)]
    ret=0
    for a in inp:
        if a == 0: continue
        ret += a*math.log(1.0/a, 2)
    #print ret, inp
    return ret

def ErrorRate(data):
    return float(min(data.count(x) for x in set(data)))/len(data)

def main(fn):
    lable = []
    with open(fn, 'rb') as csvfile:
        data = csv.reader(csvfile)
        for line in data:
            lable.append(line[-1])
    print 'entropy:',Entropy(lable[1:])
    print 'error:',ErrorRate(lable[1:])


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Wrong argv number"
