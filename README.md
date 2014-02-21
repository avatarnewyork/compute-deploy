compute-deploy
==============

compute-deploy is an Apache Libcloud wrapper used to deploy & bootstrap a cloud compute server.  You can create or download a shell script to bootstrap your server with.  See 

## Requirements

* [Python 2.7](http://www.python.org)
* [Apache Libcloud](https://libcloud.readthedocs.org) - `pip install apache-libcloud`
* [simplejson](https://github.com/simplejson/simplejson) - `pip install simplejson`
* [paramiko](https://github.com/paramiko/paramiko) - `pip install paramiko`

## Support

Currently, this version supports the following providers:

* Rackspace

## Usage

```

--size [SERVER_SIZE]
--name [SERVER_NAME]
--flavor [SERVER_OS]
--region [PROVIDER_REGION]
--bootstrap [BOOTSTRAP_FILE.sh]
--bootstrapargs [COMMA_SEPARATED_ARG_STRING]
--customfile [CUSTOMFILE_PATH]
```

## Examples

Deploy a 512MB server running CentOS 5.10 at Rackspace Chicago and bootstrap the server with [salt-bootstrap](https://github.com/saltstack/salt-bootstrap)
`./compute-deploy.py --size=512 --name=saltbox1 --flavor='CentOS 5.10' --region=ord --bootstrap='salt-bootstrap/bootstrap-salt.sh'`

Deploy a 512MB server running CentOS 6.5 at Rackspace Chicago and bootstrap the server with [puppet-bootstrap](https://github.com/avatarnewyork/puppet-bootstrap) with the puppetmaster IP being 192.168.1.1 and the puppet environment being production
`./compute-deploy.py --size=512 --name=puppetclient1 --flavor='CentOS 6.5' --region=ord --bootstrap='puppet-bootstrap/puppet-bootstrap.py' --bootstrapargs='192.168.1.1,production'`

Deploy a 512MB server running CentOS 6.5 at Rackspace Chicago and bootstrap the server with [puppet-bootstrap](https://github.com/avatarnewyork/puppet-bootstrap) with the puppetmaster IP being 192.168.1.1 and the puppet environment being production and create / mount 1GB swap disk
`./compute-deploy.py --size=512 --name=puppetclient1 --flavor='CentOS 6.5' --region=ord --bootstrap='puppet-bootstrap/puppet-bootstrap.py' --bootstrapargs='192.168.1.1,production,swap.sh' --customfile='swap.sh'`


## Bootstrap Plugins

A bootstrap plugin is any shell script you want the server to initialize with.  To use a bootstrap plugin, download or create a shell file within the compute-deploy directory and call it with the `--boostrap` flag.

### Available Bootstrap Plugins

* [salt-bootstrap](https://github.com/saltstack/salt-bootstrap)
* [puppet-bootstrap](https://github.com/avatarnewyork/puppet-bootstrap)

### Using a bootstrap plugin submodule

1. cd to the `compute-deploy` dir
2. add the submodule (ex: `git submodule add git@github.com:saltstack/salt-bootstrap.git`)
3. run: `git submodule init`
4. run: `git submodule update`
3. use the shell file provided by the plugin (ex: `--bootstrap='salt-bootstrap/bootstrap-salt.sh'`)

## Troubleshooting 

### RuntimeError: No CA Certificates were found

This is probably the most common error you may run into when first trying out the program.  This is apache-libcloud complaining that it can't find a valid certificate bundle.  **See https://libcloud.readthedocs.org/en/latest/other/ssl-certificate-validation.html** for more information.  The easiest workaround I found was as follows:

1. run this gist: https://gist.github.com/1stvamp/2158128 (this downloads and installs the ca-bundle.crt under `/usr/share/curl`)
2. set the `SSL_CERT_FILE` parameter before execute as follows:

```bash
SSL_CERT_FILE=/usr/share/curl/ca-bundle.crt python2.7 ./compute-deploy.py --size=1024 ...
```

