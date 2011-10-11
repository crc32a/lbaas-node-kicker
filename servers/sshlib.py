import traceback
import paramiko
import socket
import time
import sys
import new
import os


def fprintf(fp,format,*args): fp.write(format%args)
def printf(format,*args): sys.stdout.write(format%args)

BUFSIZE = 4096
DEBUG    = False

class Ssh(object):
    def __init__(self,*args,**kw):
        self.user = kw.get("user",None)
        self.passwd = kw.get("passwd",None)
        self.host = kw.get("host",None)
        self.port = kw.get("port",22)
        self.timeout = kw.get("timeout",None)
        self.debug = kw.get("debug",False)
        self.error_fp = kw.get("error_fp",sys.stderr)
        self.sock = None
        self.transport = None

    def open(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        if self.timeout:
            self.sock.settimeout(timeout)
        self.sock.connect((self.host,self.port))
        if self.debug:
            fprintf(self.error_fp,"Socket created\n")
            self.error_fp.flush()
        self.transport = paramiko.Transport(self.sock)
        self.transport.connect(username=self.user,password=self.passwd)

    def close(self):
        self.transport.close()
        self.sock.close()
        self.sock = None
        self.transport = None

    def shell(self,*args,**kw):
        channel = self.transport.open_session()
        combine = kw.pop("combine",False)
        if kw.has_key("term"):
            channel.get_pty(*args,**kw)
        channel.invoke_shell()
        new_method = new.instancemethod(drain,channel,channel.__class__)
        setattr(channel,"drain",new_method)
        new_method = new.instancemethod(ready,channel,channel.__class__)
        setattr(channel,"ready",new_method)
        return channel

    def execute(self,cmd,combine=False):
        channel = self.transport.open_session()
        channel.set_combine_stderr(combine)
        channel.exec_command(cmd)
        new_method = new.instancemethod(drain,channel,channel.__class__)
        setattr(channel,"drain",new_method)
        new_method = new.instancemethod(ready,channel,channel.__class__)
        setattr(channel,"ready",new_method)
        return channel

# The below method is appendend to the Paramiko.Channel object return
# by the Ssh.shell method

def ready(self):
    out = {}
    out["recv"] = self.recv_ready()
    out["recv_stderr"] = self.recv_stderr_ready()
    out["send"] = self.send_ready()
    return out

def drain(self,stderr=False,nbytes=None,bufsize=BUFSIZE):
    out = ""
    if stderr==True:
        recv = self.recv_stderr
        ready = self.recv_stderr_ready
    else:
        recv = self.recv
        ready = self.recv_ready
    while ready():
        if nbytes != None:
            data = recv_method(min(nbytes,bufsize))
            nbytes -= len(data)
            out += data
            if nbytes<=0:
                return out
        else:
            out += recv(bufsize)
    return out
            
