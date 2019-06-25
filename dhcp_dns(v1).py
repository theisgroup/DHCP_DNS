# Copyright (c) 1999-2018, Juniper Networks Inc.
# All rights reserved.
#

from junos import Junos_Context
from junos import Junos_Trigger_Event

def fnDEBUG(bDEBUGGING = False, sOutput):
    sDebugFileName = "/var/tmp/DHCP_DNS_DEBUG.log"
    sLogFileName = "/var/log/DHCP_DNS.log"
    if not(bDEBUGGING):
        hLOG_FO = open(sLogFileName, "a")
        hLOG_FO.write(sOutput)
        hLOG_FO.close()
    hDEBUG_FO = open(sDebugFileName, "a")
    hDEBUG_FO.write(sOutput)
    hDEBUG_FO.close()
    return;

def fnDoDNS(sDO, sIPAddress):
    sDNSCacheFileName = "/var/log/DNS_CACHE.log"
    sJDHCPDLogFile = "/var/log/jdhcpd"
    if sDO = "ADD":
        hDNSCache.open(sDNSCacheFileName, "a")
        # retrieve hostname from jdhcpd
        #delete jdhcpd log file
        hDNSCache.write(sHostName, sIPAddress)
        hDNSCache.close()
    else:
        with open(sDNSCacheFileName, "r") as hDNSCache:
            sLINES = hDNSCache.readlines()
        with open(sDNSCacheFileName, "r") as hDNSCache:
            for sLINE in sLINES:
                if !(sIPAddress in sLINE):
                    hDNSCache.write(line)
                #remove from config           
        hDNSCache.open(sDNSCacheFileName, "r")
        hDNSCache.close() 
    return;       

def fnDNS(sFunction, sIPAddress):
    if "DH_SVC_V4_SERVER_LEASE_TIMEOUT" in sFunction:
        fnDEBUG(sOutput = "-----DHCP LEASE TIMEOUT----------\n")
        # remove host from config
        # remove host from cache file
    if "DH_SVC_V4_SERVER_RCV_RELEASE" in sFunction:
        fnDEBUG(sOutput = "-----DHCP RELEASE--------\n")
        # remove host from config
        # remove host from cache file
    if "DH_SVC_V4_SERVER_GET_BOUND" in sFunction:
        fnDEBUG(sOutput = "-----DHCP BOUND----------\n")
        # add host to config
        # add host to cache file
    return;

def main():
    bDEBUGGING = True


    if bDEBUGGING:
        fnDEBUG(bDEBUGGING, "Junos context info: \n")
        fnDEBUG(bDEBUGGING, "*************************\n")
        fnDEBUG(bDEBUGGING, str(Junos_Context) + "\n")
        fnDEBUG(bDEBUGGING, "*************************\n")

    if bDEBUGGING:
        fnDEBUG(bDEBUGGING, "*************************\n")
        fnDEBUG(bDEBUGGING, "Triggering event details: \n")
        fnDEBUG(bDEBUGGING, "*************************\n")
        fnDEBUG(bDEBUGGING, "id: " + str(Junos_Trigger_Event.xpath('//trigger-event/id')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "type: " + str(Junos_Trigger_Event.xpath('//trigger-event/type')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "generation-time: " + str(Junos_Trigger_Event.xpath('//trigger-event/generation-time')[0].text))
        fnDEBUG(bDEBUGGING, "process-name: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/name')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "process-pid: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/pid')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "hostname: " + str(Junos_Trigger_Event.xpath('//trigger-event/hostname')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "facility: " + str(Junos_Trigger_Event.xpath('//trigger-event/facility')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "severity: " + str(Junos_Trigger_Event.xpath('//trigger-event/severity')[0].text) + "\n")
        fnDEBUG(bDEBUGGING, "message: " + str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text) + "\n")

    sEventMessage = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[0].split(":")[0]).replace(" ","")
    sClientMac = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[2]).split(" ")[2].replace(" ","")
    sClientIP = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[3]).split(" ")[2].replace(" ","")

    fnDEBUG(sOutput = "*************************\n")
    fnDEBUG(sOutput = "CLIENT INFO: \n")
    fnDEBUG(sOutput = "*************************\n")
    fnDEBUG(sOutput = "EVENT: " + sEventMessage + "\n")
    fnDEBUG(sOutput = "MAC: " + sClientMac + "\n")
    fnDEBUG(sOutput = "IP: " + sClientIP + "\n")

    if bDEBUGGING:
        fnDEBUG(bDEBUGGING, "*************************\n")
        fnDEBUG(bDEBUGGING, "DHCP PROCESS: \n")
        fnDEBUG(bDEBUGGING, "*************************\n")
    fnDNS(sEventMessage, sClientIP)
    if bDEBUGGING:
        fnDEBUG(bDEBUGGING, "\n")

 
if __name__ == '__main__':
    main()

