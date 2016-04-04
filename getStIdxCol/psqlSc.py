#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# av.pankratev
#
import sys, re, copy, pdb, os, psycopg2, psycopg2.extras, datetime, logging, time, locale, codecs, pickle
# VARIABLES
## Communications error in the input data
noarg='''\n\n\nArguments are entered incorrectly!\n\n\n1) To take a base structure, enter the settings from the first to fifth: ( host, port, dbname, user, password ).
2) To see the difference in the structure of the database, enter the six parameters: ( diff ).\n
Example:\n
1) To take a base structure, run script: ./psqlSc.py  'host' 'port' 'dbname' 'username' 'password'\n
2) To see the difference in the structure of the database: ./psqlSc.py  'host' 'port' 'dbname' 'username' 'password' diff'''
## a variable for the path
# fp=os.path.dirname(sys.argv[0])
# result=os.path.join(fp,"resultSqlSt.txt")
residxSql='/opt/scripts/resultidxSqlSt.bin'
rescolSql='/opt/scripts/resultcolSqlSt.bin'
## time now
time=str('| Beginning script excecution at %s |' % str(datetime.datetime.now()))
## variable for request index
allIndex = """
    SELECT schemaname, relname, indexrelname FROM pg_stat_all_indexes WHERE schemaname !~ '^(pg)'
"""
## variable for request column name
allColumn = """
    SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema NOT IN ('pg_catalog', 'information_schema')  ORDER BY table_schema
"""
## variable data for the database connection
try:
    CONNDB = str("host={0} port={1} dbname={2} user={3} password={4}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
except:
    print(noarg)
    sys.exit()
## variable stars
stars=''.rjust(130, '*')
# Print border
def Border(st):
    return '-'*len(st)
# Connecting to database
def Conn(d=CONNDB):
    global cur
    try:
        db_conn = psycopg2.connect(d)
        db_conn.autocommit = True
        cur = db_conn.cursor()
    except Exception as e:
        print('I can not connect to the database, an error:', e)
        sys.exit(0)
# withdrawal of exceptions to the console
def TryPrint(s):
    try:
        print(s)
    except Exception as e:
        print('It did not happen to bring the console dumps error:', e)
# parse request
def ReguData(dt):
    ## the variable will be used to name the current table
    table_list = {}
    Conn()
    ## carry out an inquiry, if not executed display exception
    try:
        cur.execute(dt)
    except Exception as e:
        print("I can't SELECT, due to : ", e)
    while (1):
        ## reads a line from the answer to a SQL query
        row = cur.fetchone()
        if row is None :
            # we exit the loop if all read
            break
        ## fill in reference indices
        if str(row[0]) in table_list:
            table_list[row[0]].setdefault(str(row[1]), []).append(str(row[2]))
        else:
            table_list[row[0]]={row[1]:[row[2]]}
    return table_list
    cur.close()
    # output in the console and write to a log
# reporting resultat
def OutputLog(typ):
    def Out(inp):
        for s in inp:
            print(stars)
            print("Name schema: %s \n" % (s))
            for table, idx  in inp[s].items():
                if isinstance(idx, (dict, list)):
                    if typ=='col':
                        print(" Table name: %s \n The number of column on the table: %s \n Column name: %s \n\n" % (table, len(idx), idx))
                    elif typ=='idx':
                        print(" Table name: %s \n The number of indexes on the table: %s \n Name index: %s \n\n" % (table, len(idx), idx))
                else:
                    print("Error type!")
    return Out
def GetSqlSt(ilog=residxSql,clog=rescolSql):
    ## border variables
    print("We provide for the - host:",sys.argv[1]," base:",sys.argv[3],"\n")
    tx='|  Print index name  |'
    br=Border(str(tx))
    txn='|  Print column name  |'
    brn=Border(str(txn))
    # TryPrint(br)
    # TryPrint(tx)
    # TryPrint(br+'\n')
    # We write and print indexes
    tableidx=ReguData(allIndex)
    # col=OutputLog('idx')
    # col(tableidx)
    logidx = Logging(ilog)
    logidx.write(tableidx)
    logidx.close()
    # TryPrint(brn)
    # TryPrint(txn)
    # TryPrint(brn+'\n')
    # write and output table Column
    tablecol=ReguData(allColumn)
    # col=OutputLog('col')
    # col(tablecol)
    logcol=Logging(clog)
    logcol.write(tablecol)
    logcol.close()
    print("The database structure information recorded!\nIndex file:",residxSql,"\nColumns of data file:",rescolSql,"\n")
def mymapPad(*seqs, pad=None):
    seqs = [list(S) for S in seqs]
    res = []
    while any(seqs):
        res.append(tuple((S.pop(0) if S else pad) for S in seqs))
    return res
# We read patterns and deduce the difference
def DiffSqlSt(log,newdata):
    log = Logging(log)
    dataold=log.load()
    dtoldtab={ y for x in dataold for y in dataold[x] }
    datanew=ReguData(newdata)
    dtnewtab={ y for x in datanew for y in datanew[x] }
    dtnewschem={x for x in datanew }
    dtoldschem={x for x in dataold }
    datatab=set(dtoldtab)|set(dtnewtab)
    data=set(dtnewschem)|set(dtoldschem)
    for i in data:
        tx=str('|  Schema name: {0} |'.format(i))
        br=Border(str(tx))
        TryPrint(br)
        TryPrint(tx)
        TryPrint(br+'\n')
        for s in datatab:
            try:
                datadiffnew=set(datanew[i][s])-set(dataold[i][s])
            except KeyError:
                try:
                    datadiffnew=set(datanew[i][s])
                except KeyError:
                    datadiffnew=set()
            try:
                datadiffold=set(dataold[i][s])-set(datanew[i][s])
            except KeyError:
                try:
                    datadiffold=set(dataold[i][s])
                except KeyError:
                    datadiffold=set()
            if datadiffnew.__len__() > 0 :
                print("Таблица: {0} -- Добавленно: {1} ".format(s,datadiffnew))
            if datadiffold.__len__() > 0 :
                print("Таблица: {0} -- Удаленно: {1} ".format(s,datadiffold))
    log.close()
# for logging class
class Logging:
   ## constructor
   def __init__(self, log):
      self.logf = log
   ## return log name
   def log_file_name(self):
      return self.logf
   ## write to a result file
   def write(self, msg):
      self.fres = open( self.log_file_name(), "wb" )
      pickle.dump(msg,  self.fres)
   ## open log
   def load(self):
      self.fres = open( self.log_file_name(), "rb" )
      data_new =  pickle.load(self.fres)
      return data_new
   ## close to a log
   def close(self):
      self.fres.close()
# We begin to dance
if __name__ == '__main__':
    ##  a variable the Border dates
    bordertime=Border(time)
    if len(sys.argv)==6:
        TryPrint(bordertime)
        TryPrint(time)
        TryPrint(bordertime+'\n')
        GetSqlSt()
    elif (len(sys.argv)==7 and sys.argv[6] == "diff"):
        print('\n\nРазница в индексах:' )
        DiffSqlSt(residxSql,allIndex)
        print('\n\nРазница в колонках:')
        DiffSqlSt(rescolSql,allColumn)
        print('\n\n\n')
    else :
        TryPrint(noarg)
