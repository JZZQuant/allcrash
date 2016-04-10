import httplib
import urlparse
import socks
import urllib2
import urllib
import random
import time
from bs4 import BeautifulSoup
from string import ascii_lowercase
import stem
import stem.connection
from stem import Signal
from stem.control import Controller
import math
from torsock import SocksiPyHandler
import constants
from Queue import Queue
from threading import Thread, Condition, Lock
from threading import active_count as threading_active_count
from pymongo import MongoClient
import pymongo
import datetime
from threading import Thread

#renew require opener only
ticker=0

class opener(object):
    
    def __init__(self,i):
            self.index=i
            self.base_port=constants.base_port+i
            self.control_port=constants.control_port+i
            self.open_socket=urllib2.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5,'localhost', self.base_port))
                                             
    def renew(self,force,count):
        try:
            if not force:
                #zeta bluff
                if random.randint(0,math.floor(math.sqrt(constants.coupons))) == 1:
                    return
            #poisson normal load balancing
            with Controller.from_port(port = self.control_port,address="127.0.0.1") as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                controller.close()
                time.sleep(0.1)
                #print "RENEW SUCCEDED ON PORT: "+ str(self.control_port)
        except Exception, e:
            if count <5:
                self.renew(force,count+1)
            else:
                pass
                #print "RENEW FAILED ON PORT: " + str(self.control_port)
                #print "attempt: "+ str(count)
                #print " error: " +str(e)
            
class Worker(Thread):
    def __init__(self,w_opener):
        Thread.__init__(self)
        self.w_opener=w_opener  
     
    def randomopener(self,myurl):
        global ticker
        cur_opener=self.w_opener.open_socket
        cur_opener.addheaders = [('User-agent', random.choice(constants.user_agent_list))]
        try:
            #f = cur_opener.open(myurl)
            Thread(target=cur_opener.open, args=[myurl]).start()
            if random.randint(1,constants.coupon_collection_rate)==1:
                self.w_opener.renew(False,0)
                print("urls served: "+str(ticker))
            ticker=ticker+1
        except Exception, e:
            #print("error while openning url")
            #print(e)
            return -1       
            
    def run(self):
        while True:
            url = constants.start
            soup = self.randomopener(url)
            #print(url)

def main():
    workers=[Worker(opener(i)) for i in range(constants.coupons)]
    for w in workers : w.start()
    for w in workers: w.join() 

if __name__ == '__main__':
    main()

    
