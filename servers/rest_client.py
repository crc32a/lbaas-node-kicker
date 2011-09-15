#!/usr/bin/python

import xml.dom.minidom
import pickle
import cPickle
import httplib
import urllib2
import urllib
import copy
import json
import sys
import os
import re

def printf(format,*args): sys.stdout.write(format%args)
def fprintf(fp,format,*args): fp.write(format%args)

http_re = re.compile("(.*)://([^/\:]*):?([0-9]+)?/(.*)",re.IGNORECASE)

def get_servers_url(file_name):
    key = "x-server-management-url"
    try:
        url = load_cpickle(file_name)[key]
    except IOError:
        url = ""
    except KeyError:
        url = ""
    return url

def getparams(params_in):
    params = urllib.urlencode(params_in)
    return params

def getbaseuri(url):
    m = http_re.match(url)
    if not m:
        return None
    else:
        return m.group(4)

def flatenTree(treeIn):
    out = []
    for x in treeIn:
        if type(x) == type([]):
            out.extend(flatenTree(x))
        else:
            out.append(x)
    return out

def splitTree(treeIn,sep):
    branchesOut = []
    if type(treeIn) == type([]):
        for branch in treeIn:
            branchesOut.extend(splitTree(branch,sep))
        return branchesOut
    else:
        branchesOut = treeIn.split(sep)
        return branchesOut

def splitOn(strIn,sep=[],exclude_blanks=True):
    t = copy.deepcopy(strIn)
    for s in sep:
        t = splitTree(t,s)
    if exclude_blanks:
        t = [x for x in t if x != ""]
    return t

def load_cpickle(file_name):
    file_path = os.path.expanduser(file_name)
    fp = open(file_path,"r")
    obj = cPickle.load(fp)
    fp.close()
    return obj

def save_cpickle(obj,file_name):
    file_path = os.path.expanduser(file_name)
    fp = open(file_path,"w")
    cPickle.dump(obj,fp)
    fp.close()
    return None

def load_pickle(file_name):
    file_path = os.path.expanduser(file_name)
    fp = open(file_path,"r")
    obj = pickle.load(fp)
    fp.close()
    return obj

def save_pickle(obj,file_name):
    file_path = os.path.expanduser(file_name)
    fp = open(file_path,"w")
    pickle.dump(obj,fp)
    fp.close()
    return None


def merge_dict(parent_dict,child_dict):
    dict_out = copy.deepcopy(parent_dict)
    dict_out.update(child_dict)
    return dict_out

def stripquotes(in_str):
    if in_str[0]=="\"" and in_str[-1] == "\"":
        return in_str[1:-1]
    else:
        return in_str[:]        

def argkvs(args):
    out=[]
    args = [stripquotes(arg) for arg in args]
    for arg in args:
        vals = arg.split("=")
        if len(vals) != 2:
            sys.stdout.flush()
            continue
        k = vals[0]
        v = stripquotes(vals[1])
        out.append((k,v))
    return out

def xml_attrs(collection_in):
    out = ""
    if type(collection_in)==type([]):
        for(k,v) in collection_in:
            out += "%s=\"%s\" "%(k,v)
    elif type(collection_in)==type({}):
        for (k,v) in collection_in.items():
            out += "%s=\"%s\" "%(k,v)
    return out


def json_attrs(collection_in):
    out = ""
    if type(collection_in)==type([]):
        kvs = [(k,v) for (k,v) in collection_in]
    elif type(collection_in)==type({}):
        kvs = [(k,v) for (k,v) in collection_in.items()]
    else:
        return None

    for (k,v) in kvs[:-1]:
       out += "\"%s\":%s, "%(k,jsonintorstr(v))
    (k,v) = kvs[-1]
    out += "\"%s\":%s "%(k,jsonintorstr(v))
    return out

def jsonintorstr(val):
    try:
        int(val)
        return val
    except ValueError:
        return "\"%s\""%val


def geturlattr(line):
    m = http_re.match(line)
    if not m:
        return (None,None,None,None)
    prot = m.group(1)
    host = m.group(2)
    port = m.group(3)
    pkg  = m.group(4)

    if port != None:
        port = int(port)
    return (prot,host,port,pkg)

def gethost(url):
    m = http_re.match(url)
    if not m:
        return None
    if m.group(3):
        host = "%s:%s"%(m.group(2),int(m.group(3)))
    else:
        host = m.group(2)
    return host

class RestClient(object):
    def __init__(self,*args,**kw):
        self.config = kw

    def set_config(self,*args,**kw):
        self.config = copy.deepcopy(kw)

    def send_req(self,*args,**kw):
        req = self._req(*args,**kw)
        return urllib2.urlopen(req)


    def _req(self,*args,**kw):
        opts = merge_dict(self.config,kw)
        headers = opts.get("headers")
        if not headers:
            headers = {}

        #Auth is breaking the AccountId on the URL.
        #headers["BYPASS-AUTH"]="true"
        #headers["BYPASS-VXML"]="true"
        #headers["BYPASS-VJSON"]="true"
        #headers["FORCEROLES"]="ops"
        if opts.has_key("auth_headers") and opts.has_key("auth_file"):
            auth_headers = load_cpickle(opts["auth_file"])
            for key in opts["auth_headers"]:
                if key  == "x-auth-token":
                    headers[key] = auth_headers[key]

        uri = opts.get("uri","")

        method = opts.get("method")

        baseurl = opts.get("baseurl","")
        url = u"%s%s"%(baseurl,uri)
        if self.config.has_key("getparams"):
            url += "?%s"%getparams(self.config["getparams"])

        data = opts.get("data")

        if os.path.isfile("./realm.db"):
            headers.update(load_cpickle("./realm.db"))

        if opts.get("debug"):
            printf("url=%s\ndata=%s\nheaders=%s\n",url,data,headers)
        req = urllib2.Request(url,data=data,headers=headers)
        if opts.has_key("method"):
            req.get_method = lambda: opts["method"]
        return req

class CodDec(object):
    def __init__(self,data=None):
        self.data = data

    def set_data(self,data):
        self.data = data

    def encode(self,contype):
        data = self.data
        
        if contype == "application/xml":
             return data

        if contype == "application/json":
            return json.dumps(data)

    def decode(self,contype):
        data = self.data

        if contype == "application/xml":
            return data
        elif contype == "application/json":
            try:
                val = json.loads(data)
            except ValueError:
                raise ValueError("Could not parse \"%s\" into json\n"%data)
            return val
        else:
            return "data"
        
    def pp(self,contype):
        obj = self.decode(contype)
        if contype == "application/json":
            return json.dumps(obj,indent=2)
        elif contype == "application/xml":
            return xml.dom.minidom.parseString(obj).toprettyxml().replace("\t","    ")
        else:
            return obj
             
