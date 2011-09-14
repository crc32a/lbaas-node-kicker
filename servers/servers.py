#!/usr/bin/env python

import rest_client
import base64
import urllib2
import json
import copy
import sys

def RequiresKeys(op,*required):
    required_keys = set(required)
    def decorator(func):
        def wrapper(*args,**kw):
            found_keys = set(kw.keys())
            missing_keys = required_keys - found_keys
            if len(missing_keys)>0:
                msg = "Missing keys %s for operation %s"%(missing_keys,op)
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
        return self.postRequest("/servers",obj,debug=True)

    def setPasswdServer(self,id,passwd):
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
        return self.getRequest("/servers/%i"%id,method="DELETE",noresp=True)

    def serverDetails(self):
        return self.getRequest("/servers/detail")

    def flavorTypes(self):
        return self.getRequest("/flavors/detail")

    def imageTypes(self):
        return self.getRequest("/images/detail")

    def postRequest(self,uri,data,**kwargs):
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
            msg = "Error ResponseCode = %s\n%s\n"%(e.code,e.read())
            sys.stderr.write(msg)
            return None
        if kwargs.has_key("noresp") and kwargs["noresp"]:
            return 
        return json.loads(resp.read())

    def getRequest(self,uri,*args,**kwargs):
        kw = copy.deepcopy(Servers.BaseKw)
        kw.update(kwargs)
        kw["uri"] = uri
        client = rest_client.RestClient(**kw)
        client.set_config(**kw)
        req = client._req()
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            msg = "Error ResponseCode = %s\n%s\n"%(e.code,e.read())
            sys.stderr.write(msg)
            return None
        if kwargs.has_key("noresp") and kwargs["noresp"]:
            return 
        return json.loads(resp.read())
