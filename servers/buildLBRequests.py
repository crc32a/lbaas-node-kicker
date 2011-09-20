#!/usr/bin/env python

from util import printf,fprintf
import time
import util
import urllib2
import sys
import os
import pickle

def render_json(json_reqs):
    jr = util.load_json(file_reqs)
    return jr

def load_url(file_name):
    cf = util.load_json(file_name)
    url = cf["hostUrl"]
    return url

def write_log(logStr, error, lb, code):
    fp = open("metrics.log", "a")
    fp.write("Took ")
    fp.write("%g "%logStr)
    fp.write("seconds to return response: \n")
    fp.write("%s\n"%error)
    fp.write("Response status code: %s \n"%code)
    fp.write(lb)
    fp.write("\n")
    fp.close()

def build_lbs(reqs):    
    for lb in reqs:
        with open('auth_headers.db') as pickle_file:
            data = pickle.load(pickle_file)
            token = data["x-auth-token"]
        headers = {"x-auth-token": token, "Content-type": "application/xml"}
        url = load_url("lbconfig.json")
        printf("\n\nurl=%s\ndata=%s\nheaders=%s\n",url,lb,headers)
        request = urllib2.Request(url, lb, headers) 
        try:
            start = time.time()
            resp = urllib2.urlopen(request)
            end = time.time()
            reqTime = end - start
    
            printf("%s%s%s", "Took ","%.2g"%reqTime," seconds to return a response \n")
            write_log(reqTime, lb, resp.code)
            printf("%s\n",resp.read())
        except urllib2.HTTPError, e:
            write_log(0.0, e.read(), lb, e.code)
            printf("Exception resp.code=%s\n%s\n",e.code,e.read())

if __name__ == "__main__":
    lbs = util.load_json("requests.json")
    build_lbs(lbs)   
