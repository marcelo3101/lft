# Local imports
from switch import Switch
from onos import ONOS

from global_variables import *

# Standard libraries imports
import subprocess
from os import getcwd

def createBridge(name: str): #, ip: str, gatewayIp: str):
    print(f" ... Creating switch {name}")
    nodes[name] = Switch(name, getcwd()+'/flows/'+name, '/home/pcap')
    nodes[name].run('mkdir /home/pcap > /dev/null 2>&1')
    nodes[name].instantiate(networkMode='bridge')
    print(f" ... {name} created successfully")

def createController(name: str):
    print(f" ... Creating controller {name}")
    nodes[name] = ONOS(name)
    nodes[name].instantiate()
    print(f" ... Controller {name} created successfully")



try:
    print("[LFT] Initializing demonstration")

    print(" ... Creating flows folder on host machine")
    subprocess.run("mkdir flows 2>/dev/null", shell=True)

    print(" ... Creating ONOS controllers")
    createController("c1")
    createController("c2")

    print(" ... ONOS created sucessfully, wait for initialization and press y")
    inp = ''
    while(inp != 'y'):
        inp = input(" Proceed to switch creation? [y]")
    nodes["c1"].activateONOSApps("172.17.0.2")
    nodes["c2"].activateONOSApps("172.17.0.3")

    print(" ... Creating internal and external bridges")
    createBridge("brint")
    createBridge("brext")
    print(" ... Connecting the bridges")
    nodes["brint"].connect(nodes["brext"], "brintbrext", "brextbrint")

    print(" ... Setting controllers for the bridges")
    nodes["brint"].setController("172.17.0.2", 6653)
    nodes["brext"].setController("172.17.0.3", 6653)

except Exception as e:
    raise(e)