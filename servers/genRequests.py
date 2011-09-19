#!/usr/bin/env python

from util import printf,fprintf
import random
import time
import util
import sys
import os


def getIps(file_name):
    sl = util.load_json(file_name)
    public_list = []
    private_list = []
    for server in sl.values():
        pub_ip = server["addresses"]["public"][0]
        priv_ip = server["addresses"]["private"][0]
        public_list.append(pub_ip)
        private_list.append(priv_ip)
    return {"PUBLIC":public_list , "SERVICENET":private_list}
        
def randomIp(ipList):
    return random.choice(ipList)

lb_post = \
"""<loadBalancer 
   xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
   name="%s" 
   port="%s" 
   protocol="%s">
   <virtualIps>
      <virtualIp type="%s" />
   </virtualIps>
   <nodes>
       %s
   </nodes>
</loadBalancer>"""


lb_node = \
"""    <node address="%s" port="%s" condition="ENABLED"/>
"""

def usage(prog):
    printf("Usage: will pull attributes from reqConfig.json \n")

def build_req(reqObj,ips):
    reqs = []
    lbQuan = reqObj["quantity"]
    lbName = reqObj["lbName"]
    lbPort = reqObj["lbPort"]
    lbProto = reqObj["lbProto"]
    vipType = reqObj["vipType"]
    nodePort = reqObj["nodePort"]
    healthMon = reqObj["healthMon"]
    healthMonType = reqObj["healthMonType"]
    nodeIpType = reqObj["nodeIpType"]
    nodeMin = reqObj["nodes"]["min"]
    nodeMax = reqObj["nodes"]["max"]
   
    for i in xrange(0,lbQuan+1):
        nodesStr ="" 
        n = random.randint(nodeMin, nodeMax)
         
        for j in xrange(0, n):
            ip = random.choice(ips[nodeIpType])
            nodeStr = lb_node%(ip, nodePort)
            nodesStr += "%s"%nodeStr
        
        lbStr = lb_post%(lbName + "%i"%i, lbPort, lbProto, vipType, nodesStr)
        reqs.append(lbStr + "\n\n")
    return reqs

if __name__ == "__main__":
    prog = sys.argv[0]
    if len(sys.argv)<1:
        usage(prog)
        sys.exit()
    ips = getIps("server_list.json")
    request_list = []
    configs = util.load_json("reqConfig.json")
    for config in configs:
        reqs = build_req(config,ips)
        for req in reqs:
            request_list.append(req)
 
    random.shuffle(request_list)     
   
    fp = open("requests.xml", "w")
    for reqStr in request_list:
        fp.write(reqStr) 
    fp.close()  
