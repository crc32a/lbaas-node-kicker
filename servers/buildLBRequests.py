#!/usr/bin/env python

from util import printf,fprintf
import time
import util
import urllib2
import sys
import os
import pickle

def usage(prog):
     printf("usage is %s <json_config_file>\n",prog)
     printf("\n")

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

def build_lbs(reqs,url):    
    for lb in reqs:
        h = pickle.load(open("auth_headers.db","r"))
        intended_keys = ["x-auth-token"]
        headers = {}
        headers["content-type"] = "application/xml"
        headers["accept"] = "application/xml"
        if os.path.isfile("extra_headers.json"):
            extra_headers = util.load_json("extra_headers.json")
            headers.update(extra_headers)
        for auth_key in intended_keys:
            headers[auth_key]=h[auth_key]
        printf("\n\nurl=%s\ndata=%s\nheaders=%s\n",url,lb,headers)
        request = urllib2.Request(url, lb, headers) 
        try:
            start = time.time()
            resp = urllib2.urlopen(request)
            end = time.time()
            reqTime = end - start
    
            printf("%s%s%s", "Took ","%.2g"%reqTime," seconds to return a response \n")
            write_log(reqTime, "", lb, resp.code)
            printf("%s\n",resp.read())
        except urllib2.HTTPError, e:
            msg = e.read()
            code = e.code
            printf("Error code=%s\nbody=%s\n",code,msg)
            write_log(0.0, msg, lb, code)
            printf("Exception resp.code=%s\n%s\n",e.code,e.read())

if __name__ == "__main__":
    prog = os.path.basename(sys.argv[0])
    if len(sys.argv)<2:
        usage(prog)
        sys.exit()
    config_file = sys.argv[1]
    url = util.load_json(config_file)["url"]
    lbs = util.load_json("requests.json")
    build_lbs(lbs,url)
