#encoding=utf-8
import getopt
import sys,os
import re
import glob
import math

from redis.sentinel import Sentinel

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def main():

    sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)
    sentinel.discover_master('mymaster')
    sentinel.discover_slaves('mymaster')


    sys.exit(1)


if __name__ == '__main__':
    main()
