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
    
#event format: deviceId,articleId,seen,dwell,completed,vote,share,modifiedTime
def generateData():
    global train
    fp = open("../data/all_event",'r')
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
        weight = 5.0*(float)vote + 5.0*(float)share + 1.0
        if train.has_key(device_id):
            train[device_id][article_id] = weight
        else:
            train[device_id] = dict()
            train[device_id][article_id] = weight

        line = fp.readline()
    fp.close()
    print "begin to populate training data with distinct device: %d" % (len(train))

    fp = fopen("../data/train.txt","w")
    
    for u,items in train.items():
        fp.write("%s"
        for i,pi in items.items():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)


def main():
    generateData()

    sys.exit(1)


if __name__ == '__main__':
    main()
