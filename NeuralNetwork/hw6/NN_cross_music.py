import sys
import csv
import math
import numpy as np
import time

#(5,-0.001,24.37014346)
#(5,-0.1,24.36122547)
HIDDEN_LAYER_UNIT_NUMBER = 14
ETA = 1.0
DEBUG = 0
DEBUG_FF = 0
DEBUG_BP = 0
DEBUG_UW = 0

def read_file(fn):
    with open(fn, 'r') as csvfile:
        raw_data = csv.reader(csvfile)
        data = []
        for i, line in enumerate(raw_data):
            if i == 0 and 'keys' not in fn: 
                continue
            for j in range(len(line)):
                if line[j] == 'yes': line[j] = 1.0
                elif line[j] == 'no': line[j] = 0.0
            data.append(line)
    return data

def feedforward(train_l, add_const_train, L0_weight, L1_weight):
    L0_output = np.ones((train_l, HIDDEN_LAYER_UNIT_NUMBER+1))
    L0_output[:,1:] = 1/(1+np.exp(-(add_const_train.dot(L0_weight))))
    L1_output = 1/(1+np.exp(-L0_output.dot(L1_weight)))
    if DEBUG_FF:
        print 'L0_output'
        print L0_output
        print 'L1_output'
        print L1_output
    return L0_output, L1_output

def backpropagation(L0_output, L1_output, true, L1_weight):
    L1_delta = L1_output*(1-L1_output)*(true-L1_output)
    L0_delta = L0_output*(1-L0_output)*(L1_delta.dot(L1_weight.T))
    if DEBUG_BP:
        print 'L1_delta'
        print L1_delta
        print 'L0_delta'
        print L0_delta
    return L0_delta, L1_delta

def update_weight(L0_weight, L1_weight, L0_output, add_const_train, L0_delta, L1_delta):
    L1_weight += ETA*L0_output.T.dot(L1_delta)/len(L1_weight)
    L0_weight += ETA*add_const_train.T.dot(L0_delta[:,1:])/len(L0_weight)
    if DEBUG_UW:
        print 'L0_weight'
        print L0_weight
        print 'L1_weight'
        print L1_weight
    return L0_weight, L1_weight

def Algorithm(train, true, test, test_key, dev):
    global ETA
    add_const_train = np.ones((len(train),len(train[0])+1))
    add_const_train[:,1:] = train
    train_l = len(add_const_train)
    input_n = len(train[0])
    start = time.time()
    current = time.time()
    pre_mse = float('inf')
    mse = float('inf')
    count = 0
    #mse_ary = []
    #L0_weight = 2*np.random.random((input_n+1, HIDDEN_LAYER_UNIT_NUMBER))-1
    #L1_weight = 2*np.random.random((HIDDEN_LAYER_UNIT_NUMBER+1, 1))-1
    L0_weight = 0.01*np.random.randn(input_n+1, HIDDEN_LAYER_UNIT_NUMBER)
    L1_weight = 0.01*np.random.randn(HIDDEN_LAYER_UNIT_NUMBER+1, 1)
    add_const_test = np.ones((len(test),len(test[0])+1))
    add_const_test[:,1:] = test
    while current - start <= 60:
    #for i in range(50000):
        L0_output, L1_output = feedforward(train_l, add_const_train, L0_weight, L1_weight)
        mse = sum((L1_output-true)**2)/len(L1_output)
        if mse >= pre_mse:
            #print 'Adjust ETA!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            ETA /= 2
        else:
            #if count%10 == 0:
            print mse[0]
            count += 1 
        pre_mse = mse
        L0_delta, L1_delta = backpropagation(L0_output, L1_output, true, L1_weight)
        L0_weight, L1_weight = update_weight(L0_weight, L1_weight, L0_output, add_const_train, L0_delta, L1_delta)
        current = time.time()

        L0_output, L1_output = feedforward(len(add_const_test), add_const_test, L0_weight, L1_weight)
        hit_rate = 0
        for i in range(len(L1_output)):
            if (L1_output[i] >= 0.5 and test_key[i] == 1) or (L1_output[i] < 0.5 and test_key[i] == 0):
                hit_rate += 1
        if float(hit_rate)/len(L1_output) > 0.8:
            break
    print 'TRAINING COMPLETED! NOW PREDICTING.'

    add_const_dev = np.ones((len(dev),len(dev[0])+1))
    add_const_dev[:,1:] = dev
    L0_output, L1_output = feedforward(len(add_const_dev), add_const_dev, L0_weight, L1_weight)
    #print L1_output
    for i in L1_output:
        if i >= 0.5:
            print 'yes'
        else:
            print 'no'

def main(fn1, fn2, fn3):
    data = read_file(fn1)
    train = np.array(data, dtype=float)
    #print train
    #print train/train.max(axis=0)
    true = np.array(read_file(fn2), dtype=float)
    #train = train/train.max(axis=0)
    train = (train-train.mean(axis=0))/train.std(axis=0)
    #print train
    #print true
    thr = int(len(train)*0.8)
    x = np.concatenate((train, true), axis=1)
    np.random.shuffle(x)
    train, true, test, test_key = x[:thr,:-1], x[:thr,-1:], x[thr:,:-1], x[thr:,-1:]
    #print test
    #print test_key
    dev = np.array(read_file(fn3), dtype=float)
    dev = (dev-dev.mean(axis=0))/dev.std(axis=0)
    Algorithm(train, true, test, test_key, dev)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "Wrong argv number"
