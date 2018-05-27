import sys

FourCatTrain = "4Cat-Train.labeled"
FourCatDev = "4Cat-Dev.labeled"
PartB5 = "PartB5.txt"

def main(fn):
    print 2**4
    print 2**(2**4)
    fourCatInputSpace = [   
            ['Male', 'Young', 'Yes', 'Yes'],
            ['Male', 'Young', 'Yes', 'No'],
            ['Male', 'Young', 'No', 'Yes'],
            ['Male', 'Young', 'No', 'No'],
            ['Male', 'Old', 'Yes', 'Yes'],
            ['Male', 'Old', 'Yes', 'No'],
            ['Male', 'Old', 'No', 'Yes'],
            ['Male', 'Old', 'No', 'No'],
            ['Female', 'Young', 'Yes', 'Yes'],
            ['Female', 'Young', 'Yes', 'No'],
            ['Female', 'Young', 'No', 'Yes'],
            ['Female', 'Young', 'No', 'No'],
            ['Female', 'Old', 'Yes', 'Yes'],
            ['Female', 'Old', 'Yes', 'No'],
            ['Female', 'Old', 'No', 'Yes'],
            ['Female', 'Old', 'No', 'No']
            ]
    fourCatTrain = [1]*65536
    f = open(FourCatTrain, 'r')
    for line in f:
        data = line.split()
        transformedData = []
        for i,a in enumerate(data):
            if i%2 == 0: continue
            transformedData.append(a)
        for i in range(65536):
            if fourCatTrain[i]:
                for idx in range(16):
                    if transformedData[:4] == fourCatInputSpace[idx]:
                        break
                if transformedData[-1] == 'high':
                    if ((1<<idx)&i) == 0:
                        fourCatTrain[i] = 0
                elif transformedData[-1] == 'low':
                    if ((1<<idx)&i):
                        fourCatTrain[i] = 0
    f.close()
    print len([ x for x in fourCatTrain if x == 1 ])

    f = open(fn, 'r')
    for line in f:
        data = line.split()
        transformedData = []
        for i,a in enumerate(data):
            if i%2 == 0: continue
            transformedData.append(a)
        high, low = 0, 0
        for i in range(65536):
            if fourCatTrain[i]:
                for idx in range(16):
                    if transformedData[:4] == fourCatInputSpace[idx]:
                        break
                if (1<<idx)&i:
                    high += 1
                else:
                    low += 1
        print high, low
    f.close()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "Wrong argv number"
