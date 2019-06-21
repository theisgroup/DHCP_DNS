# copyright (c) 1999-2018, Juniper Networks Inc.
# All rights reserved.
#
import logging
from junos import Junos_Context
from junos import Junos_Trigger_Event
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError
import jcs

def fnWriteToDevice(sConfiguration):
    logging.debug("fnWriteToDevice")
    hDev = Device()
    hDev.open()
    logging.debug("fnWriteToDevice : Device Open")
    hDev.bind(hCu=Config)

    # Lock the configuration, load configuration changes, and commit
    logging.info("fnWriteToDevice:  Locking the configuration")
    try:
        hDev.hCu.lock()
        logging.debug("fnWriteToDevice:  Configuration Locked")
    except LockError:
        logging.debug("fnWriteToDevice:  Error: Unable to lock configuration")
        hDev.close()
        return

    logging.info("fnWriteToDevice:  Loading configuration changes")
    try:
        if "delete" in sConfiguration:
           hDev.hCu.load(sConfiguration, format='set')
           logging.debug("fnWriteToDevice:  Delete Configuration Loaded")
        else:
           hDev.hCu.load(sConfiguration, format='set', merge = True)
           logging.debug("fnWriteToDevice:  Add Configuration Loaded")
    except ConfigLoadError as err:
        logging.debug("fnWriteToDevice:  " + err)
        logging.debug("fnWriteToDevice:  UNABLE TO LOAD CONFIGURATION CHANGES:")
        logging.debug("fnWriteToDevice: UNLOCKING THE CONFIGURATION")
        try:
           hDev.hCu.unlock()
           logging.debug("fnWriteToDevice:  Configuration Unlocked from Load Failure")
        except UnlockError:
            logging.debug("fnWriteToDevice:  Error: Unable to unlock configuration from Load Failure")
        hDev.close()
        return

    logging.info("fnWriteToDevice:  Committing the configuration")
    try:
        hDev.hCu.commit()
        logging.debug("fnWriteToDevice:  Configuration Commited")
        logging.debug("fnWriteToDevice:  " + sConfiguration)
    except CommitError:
        logging.debug("fnWriteToDevice:  Error: Unable to commit configuration")
        try:
           hDev.hCu.unlock()
           logging.debug("fnWriteToDevice:  Configuration Unlocked from Commit Failure")
        except UnlockError:
            logging.debug("fnWriteToDevice:  Error: Unable to unlock configuration from Commit Failure")
        hDev.close()
        return

    logging.debug("fnWriteToDevice:  Unlocking the configuration")
    try:
        hDev.hCu.unlock()
        logging.debug("fnWriteToDevice:  Configuration Unlocked")
    except UnlockError:
        logging.debug("fnWriteToDevice:  Error: Unable to unlock configuration")

    hDev.close()
    logging.debug("fnWriteToDevice:  Device Close")
    return

def fnDoDNS(sDO, sIPAddress):
    sHostName = "test1.domain.local"
    sDNSCacheFileName = "/var/tmp/DNS_CACHE.log"
    sJDHCPDLogFile = "/var/log/jdhcpd"
    sSetCommand = "set system services dns dns-proxy cache "
    sDeleteCommand = "delete system services dns dns-proxy cache "

    if sDO == "ADD":
        hDNSCache = open(sDNSCacheFileName, "a")
        hDNSCache.write(sHostName + " " + sIPAddress + "\n")
        logging.debug("fnDoDNS: ADDING " + sHostName + " " + sIPAddress + " INTO CACHE FILE")
        sCommand = sSetCommand + sHostName + " inet " + sIPAddress
        logging.info("fnDoDNS: " + sCommand)
        fnWriteToDevice(sCommand)
        hDNSCache.close()
    else:
        logging.debug("fnDoDNS: not and ADD")
        with open(sDNSCacheFileName, "r") as hDNSCache:
            sLines = hDNSCache.readlines()
            hDNSCache.close()
            logging.debug(sLines)
        with open(sDNSCacheFileName, "w") as hDNSCache:
            for sLine in sLines:
                if not(sIPAddress in sLine):
                    hDNSCache.write(sLine)
                else:
                    sHostName = sLine.split(" ")[0]
                    logging.debug("fnDoDNS: DELETING " + sHostName + ", " + sIPAddress + " FROM CACHE FILE")
                    sCommand = sDeleteCommand + sHostName + " inet " + sIPAddress
                    logging.info("fnDoDNS: " + sCommand)
                    fnWriteToDevice(sCommand)
                hDNSCache.close()
    return

def fnDNS(sFunction, sIPAddress):
    logging.debug("****DNS EVENT************")
    if "DH_SVC_V4_SERVER_LEASE_TIMEOUT" in sFunction:
        logging.debug("fnDNS:  DHCP LEASE TIMEOUT")
        fnDoDNS("REMOVE", sIPAddress)
    if "DH_SVC_V4_SERVER_RCV_RELEASE" in sFunction:
        logging.debug("fnDNS:  DHCP RELEASE")
        fnDoDNS("REMOVE",sIPAddress)
    if "DH_SVC_V4_SERVER_GET_BOUND" in sFunction:
        logging.debug("fnDNS: DHCP BOUND")
        fnDoDNS("ADD", sIPAddress)
    logging.debug("****DNS EVENT************")
    return;

def main():
    sLogFileName = "/var/tmp/DHCP_DNS.log"
    sDebugLevel = logging.DEBUG
    # Logging Levels:
    #    debug          logging.DEBUG
    #    info           logging.INFO
    #    warning        logging.WARNING
    #    error          logging.ERROR
    #    critical       logging.CRITICAL

    logging.basicConfig(filename = sLogFileName, level = sDebugLevel)

    logging.debug("****NEW EVENT************")
    logging.debug("Junos context info: " + str(Junos_Context))
    logging.debug("Triggering event details:")
    logging.debug("id: " + str(Junos_Trigger_Event.xpath('//trigger-event/id')[0].text))
    logging.debug("type: " + str(Junos_Trigger_Event.xpath('//trigger-event/type')[0].text))
    logging.debug("generation-time: " + str(Junos_Trigger_Event.xpath('//trigger-event/generation-time')[0].text))
    logging.debug("process-name: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/name')[0].text))
    logging.debug("process-pid: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/pid')[0].text))
    logging.debug("hostname: " + str(Junos_Trigger_Event.xpath('//trigger-event/hostname')[0].text))
    logging.debug("facility: " + str(Junos_Trigger_Event.xpath('//trigger-event/facility')[0].text))
    logging.debug("severity: " + str(Junos_Trigger_Event.xpath('//trigger-event/severity')[0].text))
    logging.debug("message: " + str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text))

    sEventMessage = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[0].split(":")[0]).replace(" ","")
    sClientMac = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[2]).split(" ")[2].replace(" ","")
    sClientIP = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[3]).split(" ")[2].replace(" ","")
    if ("DH_SVC_V4_SERVER_RCV_RELEASE" or "DH_SVC_V4_SERVER_LEASE_TIMEOUT") in sEventMessage:
        sClientIP = sClientIP[:len(sClientIP)-1]

    logging.info("****CLIENT INFO**********")
    logging.info("EVENT: " + sEventMessage)
    logging.info("MAC: " + sClientMac)
    logging.info("IP: " + sClientIP)
    logging.info("****CLIENT INFO**********")

    fnDNS(sEventMessage, sClientIP)

    logging.debug("****END EVENT ***********")
if __name__ == '__main__':
    main()
