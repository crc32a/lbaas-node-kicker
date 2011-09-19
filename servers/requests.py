#!/usr/bin/env python

import json

accesslist_post_xml_bad = \
"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<accessList xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
  <networkItem address="206.160.165.40" ipVersion="IPV4" type="ALLOW"/>
  <networkItem address="::1/128" ipVersion="IPV4" type="DENY"/>
  <networkItem address="206.160.165.0/24" ipVersion="IPV6" type="DENY"/>
  <networkItem address="206.160.165.0/24" ipVersion="IPV4"/>
  <networkItem type="DENY"/>

</accessList>"""

accesslist_post_json_bad = json.dumps({
  "networkItem": [
    {
      "@address": "206.160.165.40",
      "@ipVersion": "IPV4",
      "@id": "1000",
      "@type": "ALLOW"
    },
    {
      "@address": "206.160.165.0/24",
      "@ipVersion": "IPV4",
      "@id": "1001",
      "@type": "DENY"
    },
    {
      "@address": "::1/128",
      "@ipVersion": "IPVg",
      "@id": "1001",
      "@type": "DENY"
    }

  ]
})

accesslist_post_xml_good = \
"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<accessList xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
  <networkItem address="206.160.165.40" ipVersion="IPV4" type="ALLOW"/>
  <networkItem address="206.160.165.0/24" ipVersion="IPV4" type="DENY"/>
</accessList>"""

accesslist_post_json_good = \
"""{
  "networkItem": [
    {
      "@address": "206.160.165.40", 
      "@ipVersion": "IPV4", 
      "@id": "1000", 
      "@type": "ALLOW"
    }, 
    {
      "@address": "206.160.165.0/24", 
      "@ipVersion": "IPV4", 
      "@id": "1001", 
      "@type": "DENY"
    }
  ]
}
"""

hm_req = \
"""<healthMonitor 
xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
%s />
"""

hmc_post_xml_good = \
"""<healthMonitor type="CONNECT" delay="10" timeout="10" attemptsBeforeDeactivation="3" />
"""

hmc_put_xml_good = \
"""<healthMonitor xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" type="CONNECT" delay="10" timeout="10" attemptsBeforeDeactivation="3" />
"""

nwi_put_xml_good = \
""" <networkItem xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" address="206.160.165.41" ipVersion="IPV4" type="ALLOW" />
"""

sp_post_xml_good = \
""" <sessionPersistence xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" persistenceType="HTTP_COOKIE"/>
"""

sp_post_xml_bad = \
""" <sessionPersistence xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" persistenceType="DB_COOKIE"/>
"""

lg_post_xml_good = \
"""<connectionLogging xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" />
"""

lg_post_xml_bad = \
"""<Bork xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" />
"""

hs_good_post = \
"""<?xml version="1.0" ?>
<host 
    xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
    clusterId="1" 
    coreDeviceId="SomeCoreDevice" 
    managementIp="12.34.56.78" 
    managementSoapInterface="https://SomeSoapNode.com:9090" 
    maxConcurrentConnections="5" 
    name="someName" 
    status="BURN_IN"
    trafficManagerName="zues01.blah.blah" 
    type="FAILOVER" 
    zone="B"
    />
"""

hs_put = \
"""<host %s 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" />"""
hs_bs_good_post = \
"""<backup
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0"
name="NightlyBackUp" />
"""

lb_hs_bad_put = \
"""<hosts 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
sticky="false">
<host id="1" type="ACTIVE"/>
<host id="2" type="ACTIVE"/>
<host id="3" type="ACTIVE"/>
<host it="4" type="ACTIVE"/>
</hosts>
"""

lb_hs_good_put = \
"""<hosts 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
sticky="false">
  <host id="1" type="ACTIVE" />
  <host id="2" type="ACTIVE" />
</hosts>
"""

hs_put = \
"""<host %s
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
/>"""
cl_post = \
"""<cluster
   xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0"
   name="%s"
   description="%s"
   dataCenter="%s"
   username="%s"
   password="%s" />
"""

cl_put =\
"""<cluster 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
name="aClusterName" description="aDesc"/>
"""

cl_vp_post = \
"""<virtualIps 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0">
  <virtualIp address="127.0.0.2" type="PUBLIC"/>
  <virtualIp address="127.0.0.1" type="PUBLIC"/>
</virtualIps>"""

lbm_rl_post = \
"""<rateLimit 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
ticketId="1" 
expirationTime="2010-08-17T16:27:56.543-05:00" 
maxRequestsPerSecond="1"/>
"""

lbm_rl_put = \
"""<rateLimit 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
ticketId="1"
expirationTime="2010-08-17T16:27:56.543-05:00"
maxRequestsPerSecond="1"/>
"""

lbm_vp_post = \
"""<virtualIp 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0"
type="SERVICENET"/>
"""

lbm_sp_post = \
"""<suspension 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
reason="This is the reason user was suspended." 
ticketId="1799" />
"""

lb_sp_post = \
"""<sessionPersistence 
    xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
    persistenceType="%s"/>
"""

lb_sp_post_wtf = """<sessionPersistence xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" persistenceType="HTTP_COOKIE"/>"""

lb_post = \
"""<loadBalancer 
   xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
   name="%s" 
   port="80" 
   protocol="HTTP">
   <virtualIps>
      <virtualIp type="PUBLIC" />
   </virtualIps>
   <nodes>
       %s
   </nodes>
</loadBalancer>"""

node_post =  """<node address="%s" port="80" condition="ENABLED" weight="1" />"""


lb_post_port = \
"""<loadBalancer 
   xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
   name="%s" 
   port="%s" 
   protocol="HTTP">
   <virtualIps>
      <virtualIp type="SERVICENET"/>
   </virtualIps>
   <nodes>
      <node address="%s" port="80" condition="ENABLED" weight="1" />
   </nodes>
</loadBalancer>"""

lb_post_svip = \
"""<loadBalancer 
   xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
   name="%s" 
   port="%s" 
   protocol="HTTP">
   <virtualIps>
      <virtualIp id="%s"/>
   </virtualIps>
   <nodes>
      <node address="%s" port="80" condition="ENABLED" weight="1" />
   </nodes>
</loadBalancer>"""



lb_post_nns = \
"""<loadBalancer 
   name="%s" 
   port="80" 
   protocol="HTTP" rateProfileId="1">
   <virtualIps>
      <virtualIp type="PUBLIC"/>
   </virtualIps>
   <nodes>
      <node ip="%s" port="80" condition="ENABLED" />
   </nodes>
</loadBalancer>"""


lb_ct_post = \
"""<connectionThrottle
   maxConnectionRate="%s" 
   maxConnections="%s" 
   minConnections="%s" 
   rateInterval="%s" 
   xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""

lb_nodes_post = \
"""<nodes xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
%s</nodes>"""


lb_node = \
"""    <node address="%s" port="%s" condition="%s"/>
"""


lb_node_put = \
"""<node xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" %s/>"""

mg_VirtualIpBlock = """<ns2:virtualIpBlock firstIp="%s" lastIp="%s"/>"""

mg_VirtualIpBlocks = """<ns2:virtualIpBlocks type="%s" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" xmlns:ns2="http://docs.openstack.org/loadbalancers/api/management/v1.0">%s</ns2:virtualIpBlocks>"""

phills = """<virtualIpBlocks type="PUBLIC" xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" xmlns:ns2="http://docs.openstack.org/loadbalancers/api/v1.0">                                    
  <ns2:virtualIpBlock firstIp="192.168.122.128" lastIp="192.168.122.254" />                                                                                                                                   
</virtualIpBlocks>"""
byidorname = """<byIdOrName 
xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
xmlns:ns2="http://docs.openstack.org/loadbalancers/api/v1.0" 
%s
/>
"""
lb_al_post = \
"""<accessList xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">%s
</accessList> 
"""

networkItem = """
       <networkItem address="%s" type="%s"/>"""


subnet_post = """<?xml version="1.0" ?>
<ns2:hostssubnet xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" xmlns:ns2="http://docs.openstack.org/loadbalancers/api/management/v1.0">
       <ns2:hostsubnet name="n01.zeus.something">
           <ns2:netInterface name="%s">%s</ns2:netInterface>
       </ns2:hostsubnet>
</ns2:hostssubnet>
"""

cidr_post = """	            <ns2:cidr block="%s"/>"""


invalid_jsaon = """
{"WTF:"0"}
"""

vip_post_xml = """
<virtualIp ipVersion="%s" type="%s" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>
"""

virtualIpBlocksJson = """{
  "virtualIpBlocks": [
    {
      "firstIp": "10.0.0.5", 
      "lastIp": "10.0.0.253"
    }, 
    {
      "firstIp": "172.16.0.64", 
      "lastIp": "172.16.0.128"
    }, 
    {
      "firstIp": "192.168.0.3", 
      "lastIp": "192.168.0.100"
    }
  ]
  "type": "SERVICENET",
}"""

cidrTest = """
<cidrTest ipAddress="%s" ipVersion="%s" xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0">
%s</cidrTest>
"""

bounce = {}
bounce["virtualipblock"]={}
bounce["virtualipblock"]["json"]=\
"""{
  "virtualIpBlocks": [
    {
      "firstIp": "10.0.0.5", 
      "lastIp": "10.0.0.253"
    }, 
    {
      "firstIp": "172.16.0.64", 
      "lastIp": "172.16.0.128"
    }, 
    {
      "firstIp": "192.168.0.3", 
      "lastIp": "192.168.0.100"
    }
  ]
}"""


bounce["connectionthrottle"]={}
bounce["connectionthrottle"]["xml"]=\
"""<connectionThrottle maxConnectionRate="100" 
        maxConnections="200" 
        minConnections="300" 
        rateInterval="60" 
        xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""

bounce["connectionthrottle"]["json"]=\
"""{
  "connectionThrottle": {
    "maxConnectionRate": 100, 
    "minConnections": 300, 
    "rateInterval": 60, 
    "maxConnections": 200
  }
}
"""


bounce["host"] = {}
bounce["host"]["xml"]= \
"""<?xml version="1.0" ?>
<ns2:host 
    xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" 
    xmlns:ns2="http://docs.openstack.org/loadbalancers/api/management/v1.0" 
    clusterId="1" 
    coreDeviceId="SomeCoreDevice" 
    managementIp="12.34.56.78" 
    managementSoapInterface="https://SomeSoapNode.com:9090" 
    maxConcurrentConnections="5" 
    name="someName" 
    status="BURN_IN" 
    trafficManagerName="zues01.blah.blah" 
    type="FAILOVER" 
    zone="B"
    />
"""

zeusEvent = """<zeusEvent eventType="%s" paramLine="%s" xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0"/>"""


bounce["node"]={}
bounce["node"]["xml"]=\
"""<node address="127.0.0.1" condition="ENABLED" id="64" port="80" status="ONLINE" weight="1" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""
bounce["node"]["json"]=\
"""{
  "node": {
    "status": "ONLINE", 
    "weight": 1, 
    "id": 64, 
    "address": "127.0.0.1", 
    "port": 80, 
    "condition": "ENABLED"
  }
}"""

bounce["healthmonitor"]={}
bounce["healthmonitor"]["xml"]=\
"""<healthMonitor attemptsBeforeDeactivation="10" bodyRegex=".*" delay="60" id="64" path="/" statusRegex=".*" timeout="100" type="HTTP" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""
bounce["healthmonitor"]["json"]=\
"""{
  "healthMonitor": {
    "attemptsBeforeDeactivation": 10, 
    "bodyRegex": ".*", 
    "statusRegex": ".*", 
    "delay": 60, 
    "timeout": 100, 
    "path": "/", 
    "type": "HTTP", 
    "id": 64
  }
}"""

bounce["sessionpersistence"]={}
bounce["sessionpersistence"]["xml"]=\
"""<sessionPersistence persistenceType="HTTP_COOKIE" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""

bounce["sessionpersistence"]["json"]=\
"""{
  "sessionPersistence": {
    "persistenceType": "HTTP_COOKIE"
  }
}
"""

bounce["connectionlogging"]={}
bounce["connectionlogging"]["xml"]=\
"""<connectionLogging enabled="true" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>"""

bounce["connectionlogging"]["json"]=\
"""
{
  "connectionLogging": {
    "enabled": true
  }
}
"""

bounce["nodes"]={}
bounce["nodes"]["xml"]=\
"""<nodes xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
    <node address="127.0.0.1" condition="ENABLED" id="64" port="80" status="ONLINE" weight="1"/>
    <node address="127.0.0.2" condition="ENABLED" id="64" port="443" status="ONLINE" weight="1"/>
</nodes>"""

bounce["nodes"]["json"] = \
"""{
  "nodes": [
    {
      "status": "ONLINE", 
      "weight": 1, 
      "id": 64, 
      "address": "127.0.0.1", 
      "port": 80, 
      "condition": "ENABLED"
    }, 
    {
      "status": "ONLINE", 
      "weight": 1, 
      "id": 64, 
      "address": "127.0.0.2", 
      "port": 443, 
      "condition": "ENABLED"
    }
  ]
}
"""


bounce["subnetmappings"] = {}
bounce["subnetmappings"]["xml"]= \
"""<?xml version="1.0" ?>
<ns2:hostssubnet xmlns="http://docs.openstack.org/loadbalancers/api/v1.0" xmlns:ns2="http://docs.openstack.org/loadbalancers/api/management/v1.0">
    <ns2:hostsubnet name="api-zxtm-n01.stage.dfw1.stabletransit.com">
        <ns2:netInterface name="eth0">
            <ns2:cidr block="10.69.0.0/24"/>
        </ns2:netInterface>
        <ns2:netInterface name="eth1">
            <ns2:cidr block="192.168.0.0/16"/>
            <ns2:cidr block="169.254.0.0/16"/>
        </ns2:netInterface>
    </ns2:hostsubnet>
</ns2:hostssubnet>
"""

bounce["virtualip"]={}
bounce["virtualip"]["xml"]=\
"""<virtualIp address="127.0.0.1" 
    id="1" 
    ipVersion="IPV4" 
    type="PUBLIC" 
    xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>
"""

bounce["virtualip"]["xml"]=\
"""
"""

bounce["virtualips"]={}
bounce["virtualips"]["xml"]=\
"""<virtualIps xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
    <virtualIp address="127.0.0.1" id="1" ipVersion="IPV4" type="PUBLIC"/>
    <virtualIp address="127.0.0.2" id="2" ipVersion="IPV4" type="PUBLIC"/>
</virtualIps>"""

bounce["virtualips"]["json"]=\
"""{
  "virtualIps": [
    {
      "ipVersion": "IPV_4", 
      "type": "PUBLIC", 
      "id": 1, 
      "address": "127.0.0.1"
    }, 
    {
      "ipVersion": "IPV_4", 
      "type": "PUBLIC", 
      "id": 2, 
      "address": "127.0.0.2"
    }
  ]
}
"""


bounce["loadbalancer"]={}
bounce["loadbalancer"]["xml"]=\
"""
<loadBalancer algorithm="RANDOM" port="80" protocol="HTTP" status="BUILD" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
    <virtualIps>
        <virtualIp address="127.0.0.1" id="1" ipVersion="IPV4" type="PUBLIC"/>
        <virtualIp address="127.0.0.2" id="2" ipVersion="IPV4" type="PUBLIC"/>
    </virtualIps>
    <nodes>
        <node address="127.0.0.20" condition="ENABLED" id="1" port="443" status="ONLINE" weight="1"/>
    </nodes>
    <connectionThrottle maxConnectionRate="100" maxConnections="200" minConnections="300" rateInterval="60"/>
    <accessList/>
    <cluster name="TestCluster"/>
    <connectionLogging/>
</loadBalancer>
"""

bounce["loadbalancer"]["json"]= \
"""{
  "loadBalancer": {
    "status": "BUILD", 
    "protocol": "HTTP", 
    "connectionThrottle": {
      "maxConnectionRate": 100, 
      "minConnections": 300, 
      "rateInterval": 60, 
      "maxConnections": 200
    }, 
    "algorithm": "RANDOM", 
    "connectionLogging": {}, 
    "virtualIps": [
      {
        "ipVersion": "IPV_4", 
        "type": "PUBLIC", 
        "id": 1, 
        "address": "127.0.0.1"
      }, 
      {
        "ipVersion": "IPV_4", 
        "type": "PUBLIC", 
        "id": 2, 
        "address": "127.0.0.2"
      }
    ], 
    "accessList": [], 
    "cluster": {
      "name": "TestCluster"
    }, 
    "nodes": [
      {
        "status": "ONLINE", 
        "weight": 1, 
        "id": 1, 
        "address": "127.0.0.10", 
        "port": 80, 
        "condition": "ENABLED"
      }, 
      {
        "status": "ONLINE", 
        "weight": 1, 
        "id": 1, 
        "address": "127.0.0.20", 
        "port": 443, 
        "condition": "ENABLED"
      }
    ], 
    "port": 80
  }
}"""

bounce["fault"]={}

bounce["fault"]["xml"]=\
"""<loadBalancerFault code="200" faultType="%s" xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
	<message>%s</message>
	<details>%s</details>
</loadBalancerFault>
"""

bounce["fault"]["json"]=\
"""
"""

bounce["badrequest"]={}
bounce["badrequest"]["xml"]=\
"""<?xml version="1.0" ?>
<badRequest code="400" message="TestMessage" 
        xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
        <validationErrors>
             <message>Testing</message>
             <message>1</message>
             <message>2	</message>
             <message>3</message>
        </validationErrors>
        <details>TestDetail</details>
</badRequest>

"""

bounce["badrequest"]["json"]=\
"""{
  "validationErrors": {
    "messages": [
      "Testing", 
      "1", 
      "2", 
      "3"
    ]
  }, 
  "message": "TestMessage", 
  "code": 400, 
  "details": "TestDetail"
}"""

bounce["accesslist"]={}
bounce["accesslist"]["xml"]=\
"""<accessList xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
    <networkItem address="10.0.0.0/8" id="1" ipVersion="IPV4" type="DENY"/>
    <networkItem address="192.168.0.0/24" id="2" ipVersion="IPV4" type="DENY"/>
</accessList>"""

bounce["accesslist"]["json"]=\
"""{
  "accessList": [
    {
      "ipVersion": "IPV_4", 
      "type": "DENY", 
      "id": 1, 
      "address": "10.0.0.0/8"
    }, 
    {
      "ipVersion": "IPV_4", 
      "type": "DENY", 
      "id": 2, 
      "address": "192.168.0.0/24"
    }
  ]
}
"""

bounce["byidorname"]={}
bounce["byidorname"]["xml"]="""
<byIdOrName %s 
 xmlns="http://docs.openstack.org/loadbalancers/api/management/v1.0"/>"""
bounce["byidorname"]["json"]="""
{%s}
"""

bounce["updated"]={}
bounce["updated"]["xml"]=\
"""<updated 
     time="%s" 
     xmlns="http://docs.openstack.org/loadbalancers/api/v1.0"/>
"""
bounce["updated"]["json"]=\
"""
{
  "time": "%s"
}
"""


bounce["datestuff"]={}

bounce["datestuff"]["xml"]=\
"""<datestuff xmlns:ns2="http://docs.openstack.org/loadbalancers/api/v1.0">
    <created time="%s"/>
    <updated time="%s"/>
</datestuff>
"""

bounce["datestuff"]["json"]=\
"""
{
  "updated": {
    "time": "%s"
  }, 
  "created": {
    "time": "%s"
  }
}
"""

bounce["errorpage"]={}
bounce["errorpage"]["json"]=\
"""{
  "errorpage": {
    "content": "<content><big><big><big><big><big><big><b>Error or something happened</b></big></big></big></big></big></big></content>"
  }
}"""

bounce["errorpage"]["xml"]=\
"""
<errorpage xmlns="http://docs.openstack.org/loadbalancers/api/v1.0">
    <content><![CDATA[<html><big><big><big><big><big><big><b>Error or something happened</b></big></big></big></big></big></big></html>]]></content>
</errorpage>"""
