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
W= dict()

def userSimilarity():
    global train
    global W
    item_users = dict()
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    C = dict()
    N = dict()
    count = 1
    print "the size of reverted index is %d" % len(item_users)
    for i, users in item_users.items():
        if len(users) >= 500:
            continue
        if count % 100 == 0:
            print "item_users :%d,user_count:%d" % (count,len(users))
        count +=1
        for u in users:
            if N.has_key(u):
                N[u] += 1
            else:
                N[u] = 1
            if not C.has_key(u):
                C[u] = dict()
            for v in users:
                if u == v: 
                    continue

                if C[u].has_key(v):
                    C[u][v] += 1
                else:
                    C[u][v] = 1

    c_rows = len(C)
    print "Matrix C has %d rows" % c_rows
    count = 1
    for u,related_users in C.items():
        print "%d / %d processed" % (count,c_rows)
        count += 1
        if len(related_users) == 0:
            continue
        W[u] = dict()
        for v,cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u]*N[v])
    

def calculateUserSimilarity():
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
    userSimilarity()
    print "complete user similarity matrix with %d rows" % len(W)


def recommend(user,K):
    global train
    global W

    rank = dict()
    interacted_items = train[user]

    if not W.has_key(user):
        print "specified user %s not in matrix, maybe a new user" % user
        return []
 
    lis = sorted(W[user].items(),key=lambda d:d[1],reverse=True)[0:K]
    for v_wuv in lis:    
        for i,rvi in train[v_wuv[0]].items():
            if interacted_items.has_key(i):
                continue
            if rank.has_key(i):
                rank[i] += v_wuv[1] * rvi
            else:
                rank[i] = v_wuv[1] * rvi
    return sorted(rank.items(),key = lambda d:d[1],reverse=True)[0:K] 
    

def test():
    count = 0
    unmatched_user_count = 0

    fp_out = open("../data/usercf_out.txt",'w')
    fp = open("../data/deviceIds",'r')

    deviceId = fp.readline()
    while deviceId:
        deviceId = deviceId.strip("\n")
        if not train.has_key(deviceId):
            unmatched_user_count +=1
            deviceId = fp.readline()
            continue

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
    calculateUserSimilarity()
    test()
    sys.exit(1)


if __name__ == '__main__':
    main()
