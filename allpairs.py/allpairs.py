#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import os
import re
import os.path
from ext.metacomm.combinatorics import all_pairs2 as ap
fp=os.path.dirname(sys.argv[0])

# Utility generator all_pairs
def Generator(parameters):
    combinations = list(enumerate(ap.all_pairs2(parameters)))
    return combinations

# Test function
def Foobar(fam,name,otch,date):

    pattern='([1-9]|1[01])\/(19[0-9]{2}|200[0-9]|201[0-5])'
    if bool(re.search(pattern, date)) == True:
       print(fam,name,otch,date )
       print(date)
    else:
       raise

# The core test
def Core():

    # To assign a list of choose from the options file:
    lst=[]
    for lened in  open(os.path.join(fp,"input.txt"), 'r'):
        parts=lened.rstrip().split(',')
        lst.append(parts)
    inputData = lst
    # Get combinations and parse its output:
    outputData = Generator(inputData)
    with open(os.path.join(fp,"pairs.txt"), 'w') as fH:
        lsts=[]
        s=""
        col1=0
        col2=0
        for line in outputData:
            stringData = 'Combination {}:\t{}'.format(str(line[0]), str(line[1]))
            # print(stringData)
            fH.write(stringData + '\n')
            st=repr(line[1]).lstrip('[').rstrip(']').replace('"',"").rstrip().lstrip().split(',')
            ss=list(st)
            try:
               Foobar(ss[0],ss[1],ss[2],ss[3])
               col1+=1
            except  (RuntimeError, TypeError, NameError):
               s+=format(str(ss) + '\n')
               col2+=1
        # The output of the
        print('Наборы данных, которые не прошли:')
        print(s)
        print('Всего проверок:'+format(str(col1+col2)))
        print('Удачно:'+format(str(col1)))
        print('Не удачно:'+format(str(col2)))

# Main
if __name__ == '__main__':
    try:
       open(os.path.join(fp,"input.txt"), 'r')
       print('Наборы данных, которые  прошли:')
       Core()
    except:
       print('В директорий' + fp + ' ' + 'нет фаила input.txt со списком параметров, нужно создать его и внести параметры через запятую!')
       raise SystemExit
