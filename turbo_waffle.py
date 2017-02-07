""" turbo_waffle.py - https://github.com/backwhacker/

"""

import fauxmo
import logging
import time
import os
from wakeonlan import wol
import paramiko
from subprocess import call

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

# Device name
deviceName = 'my nintendo'
# Specifiy the MAC address here.
tvMac='14:C9:13:31:C1:A2'

svr1='192.168.1.63'
usr1='pi'
cmd1='nohup emulationstation &'

class ssh_request:
    """Handles SSH commands with server, user,
      and cmd inputs
    """
    def __init__(self, svr, usr, cmd):
      self.svr = svr
      self.usr = usr
      self.cmd = cmd
      ssh = paramiko.SSHClient()
      ssh.load_system_host_keys()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(svr, username=usr)
      ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    def __init__(self, deviceName):
        self.deviceName = deviceName

    TRIGGERS = {deviceName: 52000}

    def act(self, client_address, state):
        print "State", state, "from client @", client_address
        if state == True:
            #call(["nohup", "emulationstation", "&"])
            #print "call nohup emulationstation &"
            s = ssh_request(svr1, usr1, cmd1)
            print "SSH request sent:", svr1, usr1, cmd1, "."
        if state == False:
            #os.system("ls -l")
            print "Something turned off"
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    d = device_handler(deviceName)
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
