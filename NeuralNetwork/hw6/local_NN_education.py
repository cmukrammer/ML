import sys
import csv
import math
import numpy as np
import time

#(5,-0.001,24.37014346)
#(5,-0.1,24.36122547)
HIDDEN_LAYER_UNIT_NUMBER = 10
ETA = 0.1
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
    L1_weight += ETA*L0_output.T.dot(L1_delta)
    L0_weight += ETA*add_const_train.T.dot(L0_delta[:,1:])
    if DEBUG_UW:
        print 'L0_weight'
        print L0_weight
        print 'L1_weight'
        print L1_weight
    return L0_weight, L1_weight

def Algorithm(train, true, dev, dev_key):
    global ETA
    add_const_train = np.ones((len(train),len(train[0])+1))
    add_const_train[:,1:] = train
    train_l = len(add_const_train)
    input_n = len(train[0])
    start = time.time()
    current = time.time()
    min_dev_mse = float('inf')
    min_dev_mse_test_mse = 0
    pre_mse = float('inf')
    #mse_ary = []
    #L0_weight = 2*np.random.random((input_n+1, HIDDEN_LAYER_UNIT_NUMBER))-1
    L0_weight = 0.1*np.random.randn(input_n+1, HIDDEN_LAYER_UNIT_NUMBER)
    #L1_weight = 2*np.random.random((HIDDEN_LAYER_UNIT_NUMBER+1, 1))-1
    L1_weight = 0.1*np.random.randn(HIDDEN_LAYER_UNIT_NUMBER+1, 1)
    #print L0_weight, L1_weight
    add_const_dev = np.ones((len(dev),len(dev[0])+1))
    add_const_dev[:,1:] = dev
    while current - start <= 60:
    #for i in range(50):
        L0_output, L1_output = feedforward(train_l, add_const_train, L0_weight, L1_weight)
        mse = sum((L1_output-true)**2)/len(L1_output)
        #print mse[0]
        if mse >= pre_mse:
            #print 'Adjust ETA!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            ETA /= 2
        pre_mse = mse
        L0_delta, L1_delta = backpropagation(L0_output, L1_output, true, L1_weight)
        L0_weight, L1_weight = update_weight(L0_weight, L1_weight, L0_output, add_const_train, L0_delta, L1_delta)
        current = time.time()
    
        L0_output, L1_output = feedforward(len(add_const_dev), add_const_dev, L0_weight, L1_weight)
        dev_mse = sum((L1_output*100-dev_key)**2)/len(L1_output)
        if dev_mse < min_dev_mse:
            min_dev_mse_test_mse = mse
            min_dev_mse = dev_mse
    #for i in range(len(L1_output)):
    #    print i, int(L1_output[i]*100)-int(true[i]*100)
    #print 'TRAINING COMPLETED! NOW PREDICTING.'

    add_const_dev = np.ones((len(dev),len(dev[0])+1))
    add_const_dev[:,1:] = dev
    L0_output, L1_output = feedforward(len(add_const_dev), add_const_dev, L0_weight, L1_weight)
    #print L1_output
    dev_mse = 0
    dev_mse = sum((L1_output*100-dev_key)**2)/len(L1_output)
    print 'HIDDEN_LAYER_UNIT_NUMBER', HIDDEN_LAYER_UNIT_NUMBER, 'ETA', ETA, 'mse', pre_mse, 'dev_mse', dev_mse, 'min_dev_mse',min_dev_mse, 'min_dev_mse_test_mse',min_dev_mse_test_mse
    #print L0_weight, L1_weight

def main(fn1, fn2, fn3, fn4):
    global HIDDEN_LAYER_UNIT_NUMBER
    global ETA
    data = read_file(fn1)
    train = np.array(data, dtype=float)/100
    #print train
    #print train/train.max(axis=0)
    true = np.array(read_file(fn2), dtype=float)/100
    #train = train/train.max(axis=0)
    #train = (train-train.mean(axis=0))/train.std(axis=0)
    #print train
    #print true
    dev = np.array(read_file(fn3), dtype=float)/100
    dev_key = np.array(read_file(fn4), dtype=float)
    #print dev
    #dev = (dev-dev.mean(axis=0))/dev.std(axis=0)
    #tune
    for i in range(17, 18):
        for j in range(10):
            HIDDEN_LAYER_UNIT_NUMBER = i
            ETA = 0.0125
            Algorithm(train, true, dev, dev_key)
    #verify
    #for i in range(10):
        #HIDDEN_LAYER_UNIT_NUMBER = 20
        #ETA = 0.1
        #Algorithm(train, true, dev, dev_key)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print "Wrong argv number"
