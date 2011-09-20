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

def build_lbs(reqs):    
    for lb in reqs:
        with open('auth_headers.db') as pickle_file:
            data = pickle.load(pickle_file)
            token = data["x-auth-token"]
        headers = {"bypass-auth": "true", "x-auth-token": token, "Content-type": "application/xml"}
        url = load_url("lbconfig.json")
        request = urllib2.Request(url, lb, headers) 
        try:
            resp = urllib2.urlopen(request)
            printf("%s\n",resp.read())
        except urllib2.HTTPError, e:
            printf("Exception resp.code=%s\n%s\n",e.code,e.read())

if __name__ == "__main__":
    lbs = util.load_json("requests.json")
    build_lbs(lbs)   
