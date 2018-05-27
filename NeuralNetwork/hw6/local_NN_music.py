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

MOMENTUM = 0.5
pre_L1 = None
pre_L0 = None

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
    L0_output = np.ones((train_l, HIDDEN_LAYER_UNIT_NUMBER+1))/100
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
    global pre_L1, pre_L0
    if DEBUG_UW:
        print 'delta L1 weight'
        print ETA*L0_output.T.dot(L1_delta)
        print 'delta L0 weight'
        print ETA*add_const_train.T.dot(L0_delta[:,1:])
        print 'pre_L1'
        print pre_L1
        print 'pre_L0'
        print pre_L0
    L1_weight += ETA*L0_output.T.dot(L1_delta) + MOMENTUM*pre_L1
    L0_weight += ETA*add_const_train.T.dot(L0_delta[:,1:]) + MOMENTUM*pre_L0
    pre_L1 = ETA*L0_output.T.dot(L1_delta)
    pre_L0 = ETA*add_const_train.T.dot(L0_delta[:,1:])
    if DEBUG_UW:
        print 'L0_weight'
        print L0_weight
        print 'L1_weight'
        print L1_weight
    return L0_weight, L1_weight

def Algorithm(train, true, test, test_key, dev, dev_key):
    global ETA, DEBUG_UW, DEBUG_BP, DEBUG_FF, pre_L1, pre_L0
    add_const_train = np.ones((len(train),len(train[0])+1))/100
    add_const_train[:,1:] = train
    add_const_dev = np.ones((len(dev),len(dev[0])+1))/100
    add_const_dev[:,1:] = dev
    #print add_const_train
    #print add_const_dev
    train_l = len(add_const_train)
    input_n = len(train[0])
    start = time.time()
    current = time.time()
    max_hit_rate = float('-inf')
    max_hit_rate_mse = 0
    train_max_hit_rate = float('-inf')
    train_max_hit_rate_mse = 0
    pre_mse = float('inf')
    pre_hit_rate = float('-inf')
    mse = float('inf')
    #count = 0
    #mse_ary = []
    #np.random.seed(1)
    L0_weight = 0.001*np.random.randn(input_n+1, HIDDEN_LAYER_UNIT_NUMBER)
    pre_L0 = np.zeros((input_n+1, HIDDEN_LAYER_UNIT_NUMBER))
    L1_weight = 0.001*np.random.randn(HIDDEN_LAYER_UNIT_NUMBER+1, 1)
    pre_L1 = np.zeros((HIDDEN_LAYER_UNIT_NUMBER+1, 1))
    thirtys_round = 0
    #for _ in range(9):
        #L0_weight = (2*np.random.random((input_n+1, HIDDEN_LAYER_UNIT_NUMBER))-1)
        #L0_weight = 0.01*np.random.randn(input_n+1, HIDDEN_LAYER_UNIT_NUMBER)
        #L1_weight = (2*np.random.random((HIDDEN_LAYER_UNIT_NUMBER+1, 1))-1)
        #L1_weight = 0.01*np.random.randn(HIDDEN_LAYER_UNIT_NUMBER+1, 1)
    #print L0_weight, L0_weight.mean(axis=0)
    #print L1_weight, L1_weight.mean(axis=0)
    #L0_weight /= 10
    #L1_weight /= 10
    #add_const_test = np.ones((len(test),len(test[0])+1))/10
    #add_const_test[:,1:] = test
    while current - start <= 60:
    #for i in range(1000):
        #count += 1
        L0_output, L1_output = feedforward(train_l, add_const_train, L0_weight, L1_weight)
        mse = sum((L1_output-true)**2)/len(L1_output)
        #if mse < 0.07:
        #    break
        #print mse[0]
        if mse >= pre_mse:
            #print 'Adjust ETA!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            ETA /= 2
            #print ETA
        else:
            ETA = ETA*1.05
        pre_mse = mse
        L0_delta, L1_delta = backpropagation(L0_output, L1_output, true, L1_weight)
        L0_weight, L1_weight = update_weight(L0_weight, L1_weight, L0_output, add_const_train, L0_delta, L1_delta)
        if False: #(L0_delta == 0).any() or (L1_delta == 0).any():
            print 'l0 weight'
            print L0_weight
            print 'l1 weight'
            print L1_weight
            print 'l0 output'
            print L0_output
            print 'l1 output'
            print L1_output
            print 'l0 delta'
            print L0_delta
            print 'l1 delta'
            print L1_delta
            print '=============================================================='

        current = time.time()
    
        #L0_output, L1_output = feedforward(len(add_const_test), add_const_test, L0_weight, L1_weight)
        #hit_rate = 0
        #for i in range(len(L1_output)):
            #if (L1_output[i] >= 0.5 and test_key[i] == 1) or (L1_output[i] < 0.5 and test_key[i] == 0):
                #hit_rate += 1
        #if float(hit_rate)/len(L1_output) > 0.80:
            #print hit_rate, len(L1_output)
            #break
        #check train hit rate
        L0_output, L1_output = feedforward(train_l, add_const_train, L0_weight, L1_weight)
        #print L1_output
        hit_rate = 0
        #print 'dev output'
        for i in range(len(L1_output)):
            #print L1_output[i]
            if (L1_output[i] >= 0.5 and true[i] == 1) or (L1_output[i] < 0.5 and true[i] == 0):
                hit_rate += 1
        if hit_rate > train_max_hit_rate: train_max_hit_rate_mse = mse
        train_max_hit_rate = max(hit_rate, train_max_hit_rate)
        if current - start > thirtys_round*30:
            thirtys_round += 1
            print 'train_max_hit_rate', train_max_hit_rate, 'train_max_hit_rate_mse', train_max_hit_rate_mse, 'current hit rate', hit_rate
            #print count
            #if thirtys_round > 1:
                #DEBUG_FF = 1
                #DEBUG_BP = 1
                #DEBUG_UW = 1

        #check hit rate
        L0_output, L1_output = feedforward(len(add_const_dev), add_const_dev, L0_weight, L1_weight)
        #print L1_output
        hit_rate = 0
        #print 'dev output'
        for i in range(len(L1_output)):
            #print L1_output[i]
            if (L1_output[i] >= 0.5 and dev_key[i] == 1) or (L1_output[i] < 0.5 and dev_key[i] == 0):
                hit_rate += 1
        #print 'end dev output'
        if hit_rate > max_hit_rate: max_hit_rate_mse = mse
        max_hit_rate = max(hit_rate, max_hit_rate)
        #if (pre_hit_rate > 19 and hit_rate < pre_hit_rate) or hit_rate > 20: break
        pre_hit_rate = hit_rate


    #print 'TRAINING COMPLETED! NOW PREDICTING.'
    #print 'l0 weight'
    #print L0_weight
    #print 'l1 weight'
    #print L1_weight
    ##print 'l0 output'
    ##print L0_output
    ##print 'l1 output'
    ##print L1_output
    #print 'l0 delta'
    #print L0_delta
    #print 'l1 delta'
    #print L1_delta

    add_const_dev = np.ones((len(dev),len(dev[0])+1))/100
    add_const_dev[:,1:] = dev
    #print 'add_const_dev'
    #print add_const_dev
    L0_output, L1_output = feedforward(len(add_const_dev), add_const_dev, L0_weight, L1_weight)
    #print L1_output
    hit_rate = 0
    for i in range(len(L1_output)):
        #print L1_output[i], L1_output[i] >= 0.5
        if (L1_output[i] >= 0.5 and dev_key[i] == 1) or (L1_output[i] < 0.5 and dev_key[i] == 0):
            hit_rate += 1

    print 'HIDDEN_LAYER_UNIT_NUMBER', HIDDEN_LAYER_UNIT_NUMBER, 'ETA', ETA, 'mse', mse, 'hit_rate', hit_rate, 'max_hit_rate', max_hit_rate, 'max_hit_rate_mse', max_hit_rate_mse
    print 'train_max_hit_rate', train_max_hit_rate, 'train_max_hit_rate_mse', train_max_hit_rate_mse

def main(fn1, fn2, fn3, fn4):
    global HIDDEN_LAYER_UNIT_NUMBER
    global ETA
    data = read_file(fn1)
    train = np.array(data, dtype=float)
    #print train
    #print train/train.max(axis=0)
    true = np.array(read_file(fn2), dtype=float)
    #train = train/train.max(axis=0)
    train_mean = train.mean(axis=0)
    train_std = train.std(axis=0)
    train = (train-train.mean(axis=0))/train.std(axis=0)
    #print train
    #print true
    thr = int(len(train)*1)
    x = np.concatenate((train, true), axis=1)
    #print x
    #np.random.seed(1)
    #np.random.shuffle(x)
    train, true, test, test_key = x[:thr,:-1], x[:thr,-1:], x[thr:,:-1], x[thr:,-1:]
    #print 'train'
    #print train
    #print true
    #print 'test'
    #print test
    #print test_key
    dev = np.array(read_file(fn3), dtype=float)
    #dev = (dev-dev.mean(axis=0))/dev.std(axis=0)
    dev = (dev-train_mean)/train_std
    dev_key = np.array(read_file(fn4), dtype=float)
    #tune
    #for i in range(1,16):
        #for j in (0.1,0.01,0.001):
            #HIDDEN_LAYER_UNIT_NUMBER = i
            #ETA = j
            #Algorithm(train, true, dev, dev_key)
    for i in range(4,5):
        for j in range(10):
        #for j in (2.0,1.0,0.1,0.01,0.001):
            HIDDEN_LAYER_UNIT_NUMBER = i
            ETA = 1.0
            #Algorithm(train, true, dev, dev_key)
            Algorithm(train, true, test, test_key, dev, dev_key)
    #verify
    #for i in range(10):
        #HIDDEN_LAYER_UNIT_NUMBER = 12
        #ETA = 0.1
        #Algorithm(train, true, dev, dev_key)


if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print "Wrong argv number"
