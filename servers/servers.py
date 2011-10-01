#!/usr/bin/env python

import rest_client
import urllib2
import string
import base64
import json
import copy
import sys
import os

DETAILS_CACHE_FILE = "details.json"

def load_json(json_file):
    full_path = os.path.expanduser(json_file)
    full_path = os.path.abspath(full_path)
    fp = open(full_path,"r")
    json_data = fp.read()
    fp.close()
    out = json.loads(json_data)
    return out

def save_json(json_file,obj):
    full_path = os.path.expanduser(json_file)
    full_path = os.path.abspath(full_path)
    fp = open(full_path,"w")
    out = json.dumps(obj, indent=2)
    fp.write(out)
    fp.close()


def splitpath(path):
    full_path = fullpath(path)
    return full_path.split(os.path.sep)

def dirwalk(path):
    def vfunc(flist,dirname,names):
        for name in names:
            file_path = os.path.join(dirname,name)
            if os.path.isfile(file_path):
                flist.append(file_path)
    flist = []
    os.path.walk(path,vfunc,flist)
    return flist

def stripbasedir(basedir,fulldir):
    basedir_components = splitpath(basedir)
    fulldir_components = splitpath(fulldir)
    stripeddir_components = fulldir_components[len(basedir_components):]
    striped_dir = string.join(stripeddir_components,os.path.sep)
    return striped_dir

def getSkelPersonality(path):
    out = {}
    full_path = fullpath(path)
    file_list = dirwalk(full_path)
    for file_path in file_list:
        k = stripbasedir(path,file_path)
        v = open(file_path).read()
        out[k]=v
    return out

def fullpath(path_in):
    return os.path.abspath(os.path.expanduser(path_in))

def RequiresKeys(op,*required):
    required_keys = set(required)
    def decorator(func):
        def wrapper(*args,**kw):
            found_keys = set(kw.keys())
            missing_keys = required_keys - found_keys
            if len(missing_keys)>0:
                msg = "Missing keys %s for operation %s" % (missing_keys,op)
                raise KeyError(msg)
            return func(*args,**kw)
        return wrapper
    return decorator
            
class Servers(object):
    BaseKw={
        "baseurl":rest_client.get_servers_url("./auth_headers.db"),
        "auth_file":"./auth_headers.db",
        "auth_headers":["x-auth-token"],
        "headers":{"accept":"application/json","content-type":"application/json"}
       }

    @RequiresKeys("createServer","name","imageId","flavorId")
    def createServer(self,*args,**kw):
        obj = {}
        obj["server"] = {}
        obj["server"]["name"]=kw["name"]
        obj["server"]["flavorId"]=kw["flavorId"]
        obj["server"]["imageId"]=kw["imageId"]
        if kw.has_key("personality"):
            obj["server"]["personality"]=[]
            for (k,v) in kw["personality"].items():
                row = {}
                row["path"] = k
                row["contents"] = base64.standard_b64encode(v)
                obj["server"]["personality"].append(row)
        return self.postRequest("/servers",obj,debug=False)

    def setPasswdServer(self, id, passwd):
        obj = {"server":{"adminPass":passwd}}
        return self.postRequest("/servers/%i"%id,obj,method="PUT",noresp=True)

    def serversByName(self):
        out = {}
        resp = self.serverDetails()["servers"]
        for server in resp:
            out[server["name"]] = server
        return out
        
    def deleteServer(self,id):
        kw = copy.deepcopy(Servers.BaseKw)
        return self.getRequest("/servers/%i" % id, method="DELETE", noresp=True)

    def serverDetails(self,*args,**kargs):
        cache = kargs["cache"] if kargs.has_key("cache") else True
        file_path = os.path.abspath(os.path.expanduser(DETAILS_CACHE_FILE))
        if cache and os.path.isfile(file_path):
            details = load_json(DETAILS_CACHE_FILE)
            return details
        details = self.getRequest("/servers/detail")
        if cache:
            save_json(DETAILS_CACHE_FILE,details)
        return details

    def serverDetail(self,id):
        return self.getRequest("/servers/%i"%id)

    def flavorTypes(self):
        return self.getRequest("/flavors/detail")

    def imageTypes(self):
        return self.getRequest("/images/detail")

    def postRequest(self, uri,data, **kwargs):
        kw = copy.deepcopy(Servers.BaseKw)
        kw.update(kwargs)
        kw["uri"] = uri
        kw["data"] = json.dumps(data)
        client = rest_client.RestClient(**kw)
        client.set_config(**kw)
        req = client._req()
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            msg = "Error ResponseCode = %s\n%s\n" % (e.code, e.read())
            sys.stderr.write(msg)
            return None
        if kwargs.has_key("noresp") and kwargs["noresp"]:
            return 
        return json.loads(resp.read())

    def getRequest(self, uri, *args, **kwargs):
        kw = copy.deepcopy(Servers.BaseKw)
        kw.update(kwargs)
        kw["uri"] = uri
        client = rest_client.RestClient(**kw)
        client.set_config(**kw)
        req = client._req()
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            msg = "Error ResponseCode = %s\n%s\n" % (e.code, e.read())
            sys.stderr.write(msg)
            return None
        if kwargs.has_key("noresp") and kwargs["noresp"]:
            return None
        return json.loads(resp.read())
