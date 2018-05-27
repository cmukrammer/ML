import sys
import csv
import math

ATTR = {'Party':('democrat','republican'),
        'Anti_satellite_test_ban':('y','n'),
        'Aid_to_nicaraguan_contras':('y','n'),
        'Mx_missile':('y','n'),
        'Immigration':('y','n'),
        'Superfund_right_to_sue':('y','n'),
        'Duty_free_exports':('y','n'),
        'Export_south_africa':('y','n'),
        'M1':('A','notA'),
        'M2':('A','notA'),
        'M3':('A','notA'),
        'M4':('A','notA'),
        'M5':('A','notA'),
        'P1':('A','notA'),
        'P2':('A','notA'),
        'P3':('A','notA'),
        'P4':('A','notA'),
        'F':('A','notA'),
        'grade':('A','notA'),
        'year':('before1950','after1950'),
        'solo':('yes','no'),
        'vocal':('yes','no'),
        'length':('morethan3min','lessthan3min'),
        'original':('yes','no'),
        'tempo':('fast','slow'),
        'folk':('yes','no'),
        'classical':('yes','no'),
        'rhythm':('yes','no'),
        'jazz':('yes','no'),
        'rock':('yes','no'),
        'hit':('yes','no'),
        'buying':('expensive','cheap'),
        'maint':('high','low'),
        'doors':('Two','MoreThanTwo'),
        'person':('Two','MoreThanTwo'),
        'boot':('large','small'),
        'safety':('high','low'),
        'class':('yes','no'),
        }

MyDecisionTree = {1:[],2:[]}

def Entropy(data, attrs, conditions):
    a, b, ret = 0, 0, 0
    for d in data:
        if FitConditions(d, attrs, conditions):
            if d[-1] == ATTR[attrs[-1]][0]: a += 1
            else: b += 1
    for x in (a,b):
        if x == 0: continue
        x = float(x)/sum([a,b])
        ret += x*math.log(1.0/x, 2)
    return ret

def FitConditions(data, attrs, conditions={}):
    #print conditions
    for c in conditions:
        #print data, c, conditions[c]
        if data[attrs.index(c)] != conditions[c]:
            return False
    return True

def CrossEntropy(data, attrs, a, conditions):
    number = [ [0]*2 for _ in range(2) ]
    weight = [0]*2
    r, aIndex = 0, attrs.index(a)
    for d in data:
        #print "In CrossEntropy", d, conditions
        if FitConditions(d, attrs, conditions):
            #print d, aIndex, d[aIndex], ATTR[a][0], ATTR[a][1]
            if d[aIndex] == ATTR[a][0]: 
                weight[0] += 1
                if d[-1] == ATTR[attrs[-1]][0]: number[0][0] += 1
                else: number[0][1] += 1
            else:
                weight[1] += 1
                if d[-1] == ATTR[attrs[-1]][0]: number[1][0] += 1
                else: number[1][1] += 1
    #print number, weight
    for i in range(len(number)):
        t = 0
        for a in number[i]:
            if a == 0: continue
            a = float(a)/sum(number[i])
            t += a*math.log(1.0/a, 2)
        r += (float(weight[i])/sum(weight))*t
    return r

def Count(data, attrs, conditions={}):
    a, b = 0, 0
    for d in data:
        #print "In Count", d, conditions
        if FitConditions(d, attrs, conditions):
            if d[-1] == ATTR[attrs[-1]][0]: a += 1
            else: b += 1
    return [a, b]

def FindMinCrossEntropy(data, attrs, conditions={}):
    m, minMIAttr = float('inf'), ""
    for a in attrs[:-1]:
        #print a, conditions, MutualInformation(data, attrs, a, conditions)
        t = CrossEntropy(data, attrs, a, conditions)
        #print a, t, m
        if a not in conditions and t < m:
            m = t
            minMIAttr = a
    return minMIAttr, m

def BuildDecisionTree(data, attrs, level, upperLevelCondition, conditions={}):
    if level > 2: return
    x = Count(data, attrs, conditions)
    if level == 0:
        print "[{}+/{}-]".format(x[0], x[1])
    elif level == 1:
        print "{}: [{}+/{}-]".format(upperLevelCondition, x[0], x[1])
        MyDecisionTree[1].append([conditions.copy(), x[0], x[1]])
    else:
        print "| {}: [{}+/{}-]".format(upperLevelCondition, x[0], x[1])
        MyDecisionTree[2].append([conditions.copy(), x[0], x[1]])
    a, b = FindMinCrossEntropy(data, attrs, conditions)
    c = Entropy(data, attrs, conditions)
    if a and c-b >= 0.1:
        conditions.update({a:ATTR[a][0]})
        BuildDecisionTree(data, attrs, level+1, "{} = {}".format(a, ATTR[a][0]), conditions)
        conditions[a] = ATTR[a][1]
        BuildDecisionTree(data, attrs, level+1, "{} = {}".format(a, ATTR[a][1]), conditions)
        del conditions[a]

def ErrorRate(data, attrs):
    l = len(data)
    e = 0
    #print MyDecisionTree
    for d in data:
        hit, i = 0, 0
        while not hit:
            for c in MyDecisionTree[2-i]:
                if FitConditions(d, attrs, c[0]):
                    #print d, c[0]
                    if (c[1] > c[2] and d[-1] != ATTR[attrs[-1]][0]) or (c[2] > c[1] and d[-1] != ATTR[attrs[-1]][1]):
                        e += 1
                    hit = 1
                    break
            i += 1
    return float(e)/l

def main(fn1, fn2):
    lable, attr_name = [], []
    with open(fn1, 'rb') as csvfile:
        data = csv.reader(csvfile)
        for i, line in enumerate(data):
            if i == 0: 
                attr_name = [ x.replace(' ','') for x in line ]
                continue
            lable.append(line)
    BuildDecisionTree(lable, attr_name, 0, "", {})
    print "error(train):",ErrorRate(lable, attr_name)
    lable = []
    with open(fn2, 'rb') as csvfile:
        data = csv.reader(csvfile)
        for i, line in enumerate(data):
            if i == 0: 
                attr_name = [ x.replace(' ','') for x in line ]
                continue
            lable.append(line)
    print "error(test):", ErrorRate(lable, attr_name)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print "Wrong argv number"
