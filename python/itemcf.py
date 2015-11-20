#encoding=utf-8
import getopt
import sys,os
import re
import glob

import math
from operator import itemgetter, attrgetter
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

train = dict()
test = dict()
W= dict()


def itemSimilarity():
    global train
    global W

    C = dict()
    N = dict()

    count = 0

    for u, items in train.items():
        print "%d: %s has %d items " % (count,u,len(items))
        count += 1
        for i,pi in items.items():
            if N.has_key(i):
                N[i] += 1
            else:
                N[i] = 1
            if not C.has_key(i):
                C[i] = dict()
            for j,pj in items.items():
                if i == j: 
                    continue

                if C[i].has_key(j):
                    C[i][j] += 1
                else:
                    C[i][j] = 1

    for i,related_items in C.items():
        if len(related_items) == 0:
            print "no related items"
            continue
        W[i] = dict()
        for j,cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i]*N[j])

    
    

def calculateItemSimilarity():
    global train
    count = 0
    fp = open("../data/month_event",'r')
    line = fp.readline()
    while line:
        line = line.strip("\n")
        tokens = line.split('\t')
        if len(tokens) != 8:
            print "invalid line found\n"
            line = fp.readline()
            continue

        device_id = tokens[0]
        article_id = tokens[1]
        vote = int(tokens[5])
        share = int(tokens[6])
        weight = 5.0*float(vote) + 5.0*float(share) + 1.0
        if train.has_key(device_id):
            train[device_id][article_id] = weight
        else:
            train[device_id] = dict()
            train[device_id][article_id] = weight
        if ( count % 100 ) == 0:
            print "%d:%s:%s:%f" % (count,device_id,article_id,weight)
        count += 1
        line = fp.readline()
    fp.close()
    print "get training size: %d" % (len(train))
    itemSimilarity()
    print "complete item similarity matrix with %d rows" % len(W)

def recommend(user,K):
    global train
    global W

    rank = dict()
    ru = train[user]
    if len(ru) == 0:
        return []

    for i,pi in ru.items():
        if not W.has_key(i):
            continue
        list = sorted(W[i].items(),key=lambda d:d[1],reverse=True)[0:K]
        for j,wj in list:
            if j in ru:
                continue
            if rank.has_key(j):
                rank[j] += pi*wj
            else:
                rank[j] = pi*wj

    return sorted(rank.items(),key = lambda d:d[1],reverse=True)[0:K]
    

def test():
    global train
    count = 0
    unmatched_user_count = 0

    fp_out = open("../data/itemcf_out.txt",'w')

    fp = open("../data/deviceIds",'r')
    deviceId = fp.readline()
    while deviceId:
        deviceId = deviceId.strip("\n")
        if not train.has_key(deviceId):
            unmatched_user_count +=1
            deviceId = fp.readline()
            continue
        ru = train[deviceId]
        rec_list = recommend(deviceId,10)

        str = deviceId+":["
        for i,pi in rec_list:
            str = str + "{\"articleId\":\"%s\"," % (i) 
            str = str + "\"score\":\"%s\"}," % (pi)
        str = str.rstrip(',')
        str = str + ']'
        fp_out.write(str+os.linesep)
        count +=1
        if ( count % 100 ) == 0:
            print "recommended for %d devices" % count
        deviceId = fp.readline()
    fp.close()
    fp_out.close() 
    print "total %d devices not found in training data" % unmatched_user_count

def main():
    calculateItemSimilarity()
    test()
    sys.exit(1)


if __name__ == '__main__':
    main()
