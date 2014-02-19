#!/usr/bin/python

import simplejson as json
import libcloud.security
import libcloud.compute.providers
import libcloud.compute.types
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment, FileDeployment
import os.path
import re

import sys, getopt

def main(argv):
    servername=''
    serversize=''
    serverflavor=''
    serverregion=''
    boostrapfile=''
    bootstrapargs=''
    customfile=''
    deployitems=[]
    deploybsargs=[]

    try:
        opts, args = getopt.getopt(argv,"hn:s:f:r:b:ac",["name=","size=","flavor=","region=","bootstrap=","bootstrapargs=","customfile="])
    except getopt.GetoptError:
        print 'deploy.py --name=<name> --size=<size> --flavor=<flavor> --region=<region> --bootstrap=<boostrapfile> --bootstrapargs=<bootstrapargs> --customfile=<customfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'deploy.py --name=<name> --size=<size> --flavor=<flavor> --region=<region> --bootstrap=<boostrapfile> --customfile=<customfile>'
            sys.exit()
        elif opt in ("-n", "--name"):
            servername = arg
        elif opt in ("-s", "--size"):
            serversize = arg
        elif opt in ("-f", "--flavor"):
            serverflavor = arg
        elif opt in ("-r", "--region"):
            serverregion = arg
        elif opt in ("-b", "--bootstrap"):
            bootstrapfile = arg
        elif opt in ("-a", "--bootstrapargs"):
            bootstrapargs = arg
        elif opt in ("-c", "--customfile"):
            customfile = arg

    # Import username and API key from a separate JSON file
    creds = json.loads(open('creds.json').read())

    # Rackspace
    RackspaceProvider = libcloud.compute.providers.get_driver(libcloud.compute.types.Provider.RACKSPACE)
    driver = RackspaceProvider(creds["user"], creds["key"], region=serverregion)

    # Choose size and flavor
    images = driver.list_images() # Get a list of images
    sizes = driver.list_sizes() # Get a list of server sizes
    size = [s for s in sizes if s.ram == int(serversize)][0] 
    image = [i for i in images if i.name == serverflavor][0] 

    # Pass bootstrap args to bootstrap script
    if bootstrapargs:
        deploybsargs = bootstrapargs.split(',')

    # Install Keys, Bootstrap, Custom File
    install_key = SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read())
    install_bootstrap = ScriptDeployment(open(os.path.expanduser(bootstrapfile)).read(), deploybsargs)
    if customfile:
        install_customfile = FileDeployment(customfile, '/root/'+customfile)
        deployitems = [install_key, install_customfile, install_bootstrap]
    else:
        deployitems = [install_key, install_bootstrap]
     
    # MultiDeploy with keys and bootstrap file
    multideploy = MultiStepDeployment(deployitems)
    node = driver.deploy_node(name=servername, image=image, size=size, deploy=multideploy)

    # Print the Public IP after the node is built 
    print node.public_ips[0]

if __name__ == "__main__":
   main(sys.argv[1:])
