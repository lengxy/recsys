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

def main():

    dict = {"beijing":10,"shanghai":3,"hangzhou":5,"guiyang":2}
    print sorted(dict.iteritems(), key=lambda d:d[1], reverse = True )

    dict1 = {}

    dict1["cities"] = dict
    print dict1["cities"]["hangzhou"]

    sys.exit(1)


if __name__ == '__main__':
    main()
