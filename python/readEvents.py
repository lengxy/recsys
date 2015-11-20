#encoding=utf-8
import jieba
import getopt
import sys,os
import re
import glob
import xml.dom.minidom

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def computeDf():
    dict = {}
    total = 35000
    count = 0

    fp = open('tf.txt','r')
    line = fp.readline()
    while line:
        tokens = line.split(',')
        term = tokens[0]
        docid = int(tokens[2])

        if dict.has_key(term):
            dict[term].add(docid)
        else:
            dict[term] = set([docid])

        line = fp.readline()
    print "dict size %d" % len(dict)
    for (k,v) in dict.items():
        print "%s,%d" % (k,len(v))

    fp.close()

def main():
    computeDf()
    sys.exit(1)


if __name__ == '__main__':
    main()
