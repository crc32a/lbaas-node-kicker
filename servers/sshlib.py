#!/usr/bin/python

import traceback
import paramiko
import socket
import time
import sys
import os

MAXRECV = 2048
DEBUG	= False

def exc_str():
  if "exc_type" in sys.__dict__:
    exc_type = sys.exc_type.__name__
  else:
    exc_type = ""
  if "exc_value" in sys.__dict__:
    exc_value = sys.exc_value
  else:
    exc_value = ""
  return (exc_type,exc_value)

def printf(format, *args): print format % args,
def fprintf(fp,format,*args): print >> fp,format % args,

def sshcmd(user=None,passwd=None,
           host=None,port=22,timeout=None,
           fp=sys.stdout,commands=[]
          ):
  pid = os.getpid()
  if DEBUG: 
    printf("user=%s\n",user)
  if DEBUG: 
    printf("host=%s\n",host)
  if DEBUG: 
    printf("timeout=%s\n",timeout)
  if DEBUG: 
    fprintf(fp,"Inside child [%s]\n",host)
  try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if timeout:
      sock.settimeout(timeout)
    sock.connect((host,port))
    if DEBUG: 
      fprintf(fp,"Socket Created\n")
  except:
    (exc_type,exc_value) = exc_str()
    fprintf(fp,"%s:%s\n",exc_type,exc_value)
    fp.flush()
    if fp != sys.stdout:
        fp.close()
    os._exit(1)
  try:
    if DEBUG: 
      fprintf(fp,"Starting transport\n")
    transport = paramiko.Transport(sock)
    if DEBUG: 
      fprintf(fp,"Starting connect\n")
    transport.connect(username=user,password=passwd)
    if DEBUG: 
      fprintf(fp,"Starting cmd list %s\n",commands)
    first_channel = True
    for cmd in commands:
      if DEBUG: 
        fprintf(fp,"Starting channel\n")
      channel = transport.open_session()
      if first_channel:
          #Only report if the first channel opened successfully
          fprintf(fp,"SUCCESS:CHANNEL\n")
          fp.flush()
          first_channel = False
      if timeout:
        channel.settimeout(timeout)
      if DEBUG: 
        fprintf(fp,"Executing %s\n",cmd)
      channel.exec_command(cmd)
      while True:
        if DEBUG: 
          fprintf(fp,"Getting results\n")
        response = channel.recv(MAXRECV)
        if len(response)==0:
          break #EOF on channel;
        if DEBUG: 
          printf("host[%s]pid[%i]:%s\n",host,pid,response)
          sys.stdout.flush()
        fp.write(response)
      channel.close()
    transport.close()
    sock.close()
  except:
    (exc_type,exc_value) = exc_str()
    fprintf(fp,"%s:%s\n",exc_type,exc_value)
    fp.flush()
    if fp != sys.stdout:
        fp.close()
    os._exit(1)
  if fp != sys.stdout:
    fp.close()


def pssh(user=None,passwd=None,
           host=None,port=22,timeout=None,
           commands=[]):
  (r_fd,w_fd) = os.pipe()
  pid = os.fork()
  if pid == 0:
    #child Process
    time.sleep(3)
    if DEBUG: 
      printf("pid=%i (%i,%i)\n",pid,r_fd,w_fd)
    os.close(r_fd)
    fp = os.fdopen(w_fd,"w")
    if DEBUG: 
      fp.write("CHILD STARTED pid=%i (%i,%i)\n"%(pid,r_fd,w_fd))
      fp.flush()
    sshcmd(user=user,passwd=passwd,host=host,
           port=port,timeout=timeout,fp=fp,commands=commands)
    if DEBUG: 
      time.sleep(3.0)
      fp.write("closeing connection\n")
    fp.close()
    os._exit(0)
  else:
    #parent process
    if DEBUG: 
      printf("pid=%i (%i,%i)\n",pid,r_fd,w_fd)
    os.close(w_fd)
    fp = os.fdopen(r_fd,"r")
    return (fp,pid)
