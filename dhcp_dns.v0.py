# Copyright (c) 1999-2018, Juniper Networks Inc.
# All rights reserved.
#

from junos import Junos_Context
from junos import Junos_Trigger_Event

def main():
    debugging = True

    if debugging:
        fo = open("/var/tmp/DHCP_DNS_DEBUG.log", "a")
    else:
        fo = open("/var/log/DHCP_DNS.log", "a")

    if debugging:
        fo.write("Junos context info: \n")
        fo.write("*************************\n")
        fo.write(str(Junos_Context) + "\n")
        fo.write("*************************\n")

    if debugging:
        fo.write("*************************\n")
        fo.write("Triggering event details: \n")
        fo.write("*************************\n")
        fo.write("id: " + str(Junos_Trigger_Event.xpath('//trigger-event/id')[0].text) + "\n")
        fo.write("type: " + str(Junos_Trigger_Event.xpath('//trigger-event/type')[0].text) + "\n")
        fo.write("generation-time: " + str(Junos_Trigger_Event.xpath('//trigger-event/generation-time')[0].text))
        fo.write("process-name: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/name')[0].text) + "\n")
        fo.write("process-pid: " + str(Junos_Trigger_Event.xpath('//trigger-event/process/pid')[0].text) + "\n")
        fo.write("hostname: " + str(Junos_Trigger_Event.xpath('//trigger-event/hostname')[0].text) + "\n")
        fo.write("facility: " + str(Junos_Trigger_Event.xpath('//trigger-event/facility')[0].text) + "\n")
        fo.write("severity: " + str(Junos_Trigger_Event.xpath('//trigger-event/severity')[0].text) + "\n")
        fo.write("message: " + str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text) + "\n")

    event_message = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[0].split(":")[0]).replace(" ","")
    client_mac = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[2]).split(" ")[2].replace(" ","")
    client_ip = (str(Junos_Trigger_Event.xpath('//trigger-event/message')[0].text).split(",")[3]).split(" ")[2].replace(" ","")

    fo.write("*************************\n")
    fo.write("CLIENT INFO: \n")
    fo.write("*************************\n")
    fo.write("EVENT: " + event_message + "\n")
    fo.write("MAC: " + client_mac + "\n")
    fo.write("IP: " + client_ip + "\n")

    if debugging:
        fo.write("*************************\n")
        fo.write("DHCP PROCESS: \n")
        fo.write("*************************\n")
    if "DH_SVC_V4_SERVER_RCV_RENEW" in event_message:
        fo.write("-----DHCP RENEW----------\n")
    if "DH_SVC_V4_SERVER_RCV_RELEASE" in event_message:
        fo.write("-----DHCP RELEASE--------\n")
    if "DH_SVC_V4_SERVER_GET_BOUND" in event_message:
        fo.write("-----DHCP BOUND----------\n")

    if debugging:
        fo.write("\n")

    fo.close()

if __name__ == '__main__':
    main()

