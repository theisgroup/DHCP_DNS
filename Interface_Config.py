from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jinja2 import Template
import yaml
import sys

JUNOS_HOSTS = [ '192.168.122.2']

for HOST in JUNOS_HOSTS:
    try:
        # Open and read the Jinja2 template file
        with open('Interface_Config.j2','r') as TEMPLATE_FH:
            TEMPLATE_FORMAT = TEMPLATE_FH.read()
        # Open and read the YAML file
        with open('Interface_Answ.yml','r') as ANSWER_FH:
            DATA = yaml.load(ANSWER_FH.read())
        # Associate TEMPLATE_FORMAT file with Template
        TEMPLATE = Template(TEMPLATE_FORMAT)
        # Merge the data with the Template
        TEMP_CONFIG = TEMPLATE.render(DATA)
        print "\nResults for device " + HOST
        print "------------------------------"
        print TEMP_CONFIG
        DEVICE = Device(host=HOST, user='root', password='Rachel01').open()
        CONFIG = Config(DEVICE)
        CONFIG.lock()
        #CONFIG.load(TEMP_CONFIG, merge=True, format='text') #merge existing config with this config
        CONFIG.load(TEMP_CONFIG, override=True, format='text') #
        #CONFIG.load(TEMP_CONFIG, replace=True, format='text') #
        #CONFIG.load(TEMP_CONFIG, update=True, format='text') #replaces with this config
        CONFIG.pdiff()
        CONFIG.commit()
        CONFIG.unlock()
        DEVICE.close()
    except LockError as e:
        print "The config database was locked!"
    except ConnectTimeoutError as e:
        print "Connection time out!"
 

