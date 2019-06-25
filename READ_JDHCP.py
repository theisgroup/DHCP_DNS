# copyright (c) 1999-2018, Juniper Networks Inc.
# All rights reserved.
#
import logging
import inspect
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

def fnConvertMacAddess(sMacAddress):
    sMacAddress = sMacAddress.split(":")
    sMacAddress = sMacAddress[0] + " " + sMacAddress[1] + " " + sMacAddress[2] + " " + sMacAddress[3] + " " + sMacAddress[4] + " " + sMacAddress[5]
    logging.debug("[fnConvertMacAddress] " + sMacAddress)
    return sMacAddress

def fnConvertHostName(sHostName):
    sDomainName = ".domain.local"
    iHostNameLength = 0
    sTempString =""

    sTempString = sHostName[1]
    sTempString = sTempString.split(" ")
    iHostNameLength = int(sTempString[len(sTempString)-1],base=10)
    logging.debug("[fnConvertHostName] Length of sTempString "+ str(iHostNameLength))

    sHostName = sHostName[2]
    sHostName = sHostName.split(" ")
    logging.debug("[fnConvertHostName] Length of sHostName "+ str(len(sHostName)))
    sTempString =""
    for i in range(2, iHostNameLength + 2):
        sTempString = sTempString + sHostName[i]
        logging.debug("[fnConvertHostName] " + sTempString)
    sTempString = sTempString.decode("hex")
    logging.debug("[fnConvertHostName] " + sTempString)
    return (sTempString + sDomainName)

def fnREAD_JDHCPD(sMacAddress):
    sJHCPDFileName = "/var/log/jdhcpd"
    sKeyMacAddress = "DHCP/BOOTP chaddr =="
    bMacAddressFound = False
    sKeyHostName = "OPTION code  12"
    bHostNameFound = False
    sKeyDHCPMethodEnd = "OPTION code 255"

    sMacAddress = fnConvertMacAddess(sMacAddress)
    with open(sJHCPDFileName, "r") as hJDHCPDFile:
        for sJDHCPDReadLine in hJDHCPDFile:
            logging.debug("[fnRead_JDHCPD] " + sJDHCPDReadLine)
            if sKeyMacAddress in sJDHCPDReadLine:
                logging.debug("[fnRead_JDHCPD] " + sKeyMacAddress + " Found")
                if sMacAddress in sJDHCPDReadLine:
                    logging.debug("[fnRead_JDHCPD] " + sMacAddress + " Found")
                    bMacAddressFound = True
                else:
                    bMacAddressFound = False
            if bMacAddressFound and not(sKeyDHCPMethodEnd in sJDHCPDReadLine):
                if sKeyHostName in sJDHCPDReadLine:
                    logging.debug("[fnRead_JDHCPD] " + sKeyHostName + " Found")
                    sHostName = sJDHCPDReadLine.split(",")
                    sHostName = fnConvertHostName(sHostName)
                    logging.debug("[fnRead_JDHCPD] " + sHostName + " is hostname")
            else:
                bMacAddressFound = False
    return sHostName

def main():
    sLogFileName = "/var/tmp/READ_JDHCPD.log"
    sHostName = "test1.domain.local"
    FORMAT = "[%(asctime)s:%(levelname)s:%(funcName)s ] %(message)s"
    sDebugLevel = logging.DEBUG
    # Logging Levels:
    #    notset         logging.NOTSET
    #    debug          logging.DEBUG
    #    info           logging.INFO
    #    warning        logging.WARNING
    #    error          logging.ERROR
    #    critical       logging.CRITICAL

    logging.basicConfig(format = FORMAT, datefmt='%d-%b-%y %H:%M:%S', filename = sLogFileName, level = sDebugLevel)
    sHostName = fnREAD_JDHCPD("00:0c:29:fe:49:a8")
    logging.debug(sHostName)

if __name__ == '__main__':
    main()

