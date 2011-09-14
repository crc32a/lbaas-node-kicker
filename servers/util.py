#!/usr/bin/env python
import rest_client
import urllib2
import servers
import cPickle
import string
import json
import sys
import os
import re

cmd_str  = "(\S+)\s+(\S+).*(%s)\s+(.*)"

def printf(format,*args): sys.stdout.write(format%args)

def fprintf(fp,format,*args): fp.write(format%args)

def splitpath(path):
    full_path = fullpath(path)
    return full_path.split(os.path.sep)

def joinpath(components):
    return string.join(components,os.path.sep)

def stripbasedir(basedir,fulldir):
    basedir_components = splitpath(basedir)
    fulldir_components = splitpath(fulldir)
    stripeddir_components = fulldir_components[len(basedir_components):]
    striped_dir = joinpath(stripeddir_components)
    return striped_dir

def fullpath(path_in):
    return os.path.abspath(os.path.expanduser(path_in))

def chop(line):
    return line.replace("\r","").replace("\n","")

def choplines(lines):
    lines_out = []
    for line in lines:
        lines_out.append(chop(line))
    return lines_out

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

def dirwalk(path):
    def vfunc(flist,dirname,names):
        for name in names:
            file_path = os.path.join(dirname,name)
            if os.path.isfile(file_path):
                flist.append(file_path)
    flist = []
    os.path.walk(path,vfunc,flist)
    return flist

def stripBaseList(basepath,file_list):
    return [stripbasedir(basepath,f) for f in file_list]

def getSkelPersonality(path):
    out = {}
    full_path = fullpath(path)
    file_list = dirwalk(full_path)
    for file_path in file_list:
        k = stripbasedir(path,file_path)
        v = open(file_path).read()
        out[k]=v
    return out

def getServer(*names):
    out = {}
    s = servers.Servers()
    serv_dict = s.serversByName()
    if len(names)<1:
        return serv_dict
    for key in names:
        out[key]=serv_dict[key]
    return out

        
def deleteServer(sname):
    s = servers.Servers()
    servs = s.serversByName()
    id = servs[sname]["id"]
    return s.deleteServer(id)

def setPasswdServer(config,sname,passwd):
    s = servers.Servers()
    host = getHosts(config)[sname]
    id = host["id"]
    return s.setPasswdServer(id,passwd)

def createServer(config,sname):
    s = servers.Servers()
    personality=getSkelPersonality(config["skelPath"])
    name = sname
    resp = s.createServer(name=name,imageId=config["imageId"],
           flavorId=config["flavorId"],personality=personality)
    return resp

def getHosts(config):
    hosts = {}
    host_re = getHostRe(config)
    for(k,v) in getServer().items():
        m = host_re.match(k)
        if not m:
            continue
        hosts[k]=v
    return hosts

def getHostsByNumber(config):
    out = {}
    hosts = getHosts(config)
    host_re = getHostRe(config)
    for(k,v) in hosts.items():
        m = host_re.match(k)
        if not m:
            break
        n = int(m.group(1))
        out[n]=v
    return out

def getHostRe(config):
    host_restr = "n([0-9]+)%s"
    host_re = re.compile(host_restr%(re.escape(config["baseHost"])))
    return host_re

def psAll():
    lines = os.popen("ps -ef -ww","r").readlines()
    return lines


def match_cmd(lines,cmd):
    out = {}
    cmd_r = re.escape(cmd)
    cmd_re = re.compile(cmd_str%cmd_r)
    for line in lines:
        m = cmd_re.match(chop(line))
        if m:
            pid = int(m.group(2))
            cmd_name = m.group(3)
            params = m.group(4)
            out[pid] = (m.group(3),m.group(4))
    return out

def stripBaseHost(config,host):
    baseHost = config["baseHost"]
    host_format = "(.*)%s"
    host_restr = host_format%(re.escape(config["baseHost"]))
    host_re = re.compile(host_restr)
    m = host_re.match(host)
    if not m:
        raise ValueError("%s does not match with %s"%(host,config["baseHost"]))
    return m.group(1)


    