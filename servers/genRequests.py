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
      %s
</loadBalancer>
"""


lb_node = \
"""<node address="%s" port="%s" condition="ENABLED"/>"""

hm_req = \
"""<healthMonitor type="%s" delay="10" timeout="10" attemptsBeforeDeactivation="3" />"""

def usage(prog):
    printf("Usage:Configure several json configs to build multiple loadbalancer request objects (will pull attributes from reqConfig.json) \n")

def build_req(req_obj,ips):
    reqs = []
    lb_quan = req_obj["quantity"]
    lb_name = req_obj["lbName"]
    lb_port = req_obj["lbPort"]
    lb_proto = req_obj["lbProto"]
    vip_type = req_obj["vipType"]
    node_port = req_obj["nodePort"]
    health_mon = req_obj["healthMon"]
    health_mon_type = req_obj["healthMonType"]
    nodeip_type = req_obj["nodeIpType"]
    node_min = req_obj["nodes"]["min"]
    node_max = req_obj["nodes"]["max"]
   
    for i in xrange(0,lb_quan):
        nodesStr ="" 
        n = random.randint(node_min, node_max)
         
        for j in xrange(0, n):
            ip = random.choice(ips[nodeip_type])
            nodeStr = lb_node%(ip, node_port)
            nodesStr += "%s\n    "%nodeStr
        
        if health_mon == "true":
           hm = hm_req%(health_mon_type)
        else:
           hm = "" 
        
        lbStr = lb_post%(lb_name + "%i"%i, lb_port, lb_proto, vip_type, nodesStr, hm)
        reqs.append(lbStr + "\n")
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
   
    util.save_json("requests.json", request_list)
