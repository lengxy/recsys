#encoding=utf-8
import getopt
import sys,os
import re
import glob
import xml.dom.minidom
import math

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

MAX_KEYWORDS = 10
MAX_DOC_NUM = 35000.0

def getKeywords():
    
    df_dict = {}
    doc_id = 0
    count = 0

    fp = open("df.txt",'r')

    line = fp.readline()
    while line:
        tokens = line.split(',')
        if len(tokens) != 2:
            line = fp.readline()
            continue
        term = tokens[0]
        docs = int(tokens[1])
        df_dict[term] = docs
        line = fp.readline()
    fp.close()

    fp = open("tf.txt",'r')
    fp2 = open("score.txt",'w')
    line = fp.readline()
    
    print "begin to generat score data..."
    while line:
        count += 1
        tokens = line.split(',')
        if len(tokens) != 4:
            line = fp.readline()
            continue

        term = tokens[0]
        tf = float(tokens[1])
        doc_id = tokens[2]
        term_all = float(tokens[3])
        if df_dict.has_key(term):
            df = float(df_dict[term])
        else:
            df = 0.0
        score = (tf/term_all) * math.log(MAX_DOC_NUM/(1.0+df))*100.0
        fp2.write("%s,%f,%s" % (term,score,doc_id))
        fp2.write(os.linesep)
        line = fp.readline()
    fp.close()
    fp2.close()

    print "begin to compute the final 10 keywords for each doc..."
    fp = open("score.txt",'r')
    line = fp.readline()
    
    dict1 = {}

    while line:
        tokens = line.split(',')
        if len(tokens) != 3:
            line = fp.readline()
            continue
        docId = tokens[2]
        term = tokens[0]
        score = float(tokens[1])
        if dict1.has_key(docId):
            dict1[docId][term] = score
        else:
            dict2 = {}
            dict2[term] = score
            dict1[docId] = dict2
        
        line = fp.readline()
    fp.close()

    fp = open("keyword.txt",'w')
    
    for (k,v) in dict1.items():
        dict3 = dict(v)
        lis = sorted(dict3.iteritems(),key=lambda d:d[1],reverse = True )
        count = 0
        for ts in lis:
            fp.write("%s,%s,%f" % (k.strip("\n"),ts[0],ts[1]))
            fp.write(os.linesep)
            count += 1
            if count == 10:
                break
            
    fp.close()
 
def main():
    getKeywords()
    sys.exit(1)


if __name__ == '__main__':
    main()
