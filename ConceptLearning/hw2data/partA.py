import sys

NineCatTrain = "9Cat-Train.labeled"
NineCatDev = "9Cat-Dev.labeled"
PartA6 = "partA6.txt"

def main(fn):
    print 2**9
    print 155
    print 3**9+1
    print (3**10)+1
    print (3**8)*4+1
    nineCatTrain = [None]*9
    f = open(NineCatTrain, 'r')
    pf = open(PartA6, 'w')
    count = 0
    for line in f:
        data = line.split()
        count += 1
        if data[-1] == 'high': 
            for i,a in enumerate(data):
                if i%2 == 0: continue
                else:
                    if i/2 < 9:
                        if nineCatTrain[i/2] == None:
                            nineCatTrain[i/2] = a
                        elif nineCatTrain[i/2] != a:
                            nineCatTrain[i/2] = "?"
        if count%30 == 0:
            pf.write("\t".join(nineCatTrain))
            pf.write("\n")
    f.close()
    pf.close()

    f = open(NineCatDev, 'r')
    count, miss = 0, 0
    for line in f:
        data, conflict = line.split(), 0
        for i,a in enumerate(data):
            if i%2 == 0: continue
            if i/2 < 9:
                if nineCatTrain[i/2] != "?" and a != nineCatTrain[i/2]: 
                    conflict = 1
                    break
        if conflict and data[-1] == "high" or conflict == 0 and data[-1] == "low": 
            miss += 1
        count += 1
    f.close()
    print float(miss)/count

    f = open(fn, 'r')
    for line in f:
        data, conflict = line.split(), 0
        for i,a in enumerate(data):
            if i%2 == 0: continue
            if i/2 < 9:
                if nineCatTrain[i/2] != "?" and a != nineCatTrain[i/2]:
                    conflict = 1
                    break
        if conflict: print "low"
        else: print "high"
    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Wrong argv number"
