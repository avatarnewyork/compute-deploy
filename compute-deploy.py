#!/usr/bin/python

import simplejson as json
import libcloud.security
import libcloud.compute.providers
import libcloud.compute.types
from libcloud.compute.deployment import MultiStepDeployment, ScriptDeployment, SSHKeyDeployment
import os.path

import sys, getopt

def main(argv):
    servername=''
    serversize=''
    serverflavor=''
    serverregion=''
    boostrapfile=''
    try:
        opts, args = getopt.getopt(argv,"hn:s:f:r:b:",["name=","size=","flavor=","region=","bootstrap="])
    except getopt.GetoptError:
        print 'deploy.py --name=<name> --size=<size> --flavor=<flavor> --region=<region> --bootstrap=<boostrapfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'deploy.py --name=<name> --size=<size> --flavor=<flavor> --region=<region> --bootstrap=<boostrapfile>'
            sys.exit()
        elif opt in ("-n", "--name"):
            servername = arg
        elif opt in ("-s", "--size"):
            serversize = arg
        elif opt in ("-f", "--flavor"):
            serverflavor = arg
        elif opt in ("-f", "--region"):
            serverregion = arg
        elif opt in ("-f", "--bootstrap"):
            bootstrapfile = arg

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

    # Install Keys
    install_key = SSHKeyDeployment(open(os.path.expanduser("~/.ssh/id_rsa.pub")).read())
    install_bootstrap = ScriptDeployment(open(os.path.expanduser(bootstrapfile)).read())

    # MultiDeploy with keys and bootstrap file
    multideploy = MultiStepDeployment([install_key, install_bootstrap])
    node = driver.deploy_node(name=servername, image=image, size=size, deploy=multideploy)

    # Print the Public IP after the node is built 
    print node.public_ips[0]

if __name__ == "__main__":
   main(sys.argv[1:])
