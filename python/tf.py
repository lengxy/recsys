#encoding=utf-8
import jieba
import getopt
import sys,os
import re
import MySQLdb
import glob
import xml.dom.minidom

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def readFromDB():
    dict = {}
    doc_id = 0
    total = 0

    fp = open('tf.txt','w')
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='3df119f3a3964ab4',port=3306)
        cur = conn.cursor()
        cur.execute('use meitian')
        cur.execute('set names utf8')

        cur.execute('select textContent from content')
        rows = cur.fetchall()
        for row in rows:
            total = 0
            dict.clear()
            seg_list = jieba.cut(row[0],cut_all=False)

            for term in seg_list:
                total += 1
                if dict.has_key(term):
                    dict[term]+=1
                else:
                    dict[term]=1
            for (term,termfq) in dict.items():
                line = "%s,%d,%d,%d" % (term,termfq,doc_id,total)

                fp.write(line)
                fp.write(os.linesep)
            print "Processed %d documents" % doc_id            
            doc_id += 1    
            
        fp.close()    
        cur.close()    
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0],e.args[1])



def main():
    readFromDB()
    sys.exit(1)


if __name__ == '__main__':
    main()
