# vEPC NFV Blueprint #

This repository contains a Cloudify TOSCA-based blueprint for deploying a virtualized Evolved Packet Core, the core network architecture of 3GPP's LTE wireless communication standard.


## Purpose of vEPC NFV Blueprint ##

This blueprint was created in order to demonstrate that virtualization of the core network of LTE was possible.
The TOSCA standard is used for describing all the VNFs, which are deployed by the open source cloud orchestrator [Cloudify](http://docs.getcloudify.org/4.0.0/intro/what-is-cloudify/).
By using the [AWS plugin for Cloudify](http://docs.getcloudify.org/4.0.0/plugins/aws/), we are able to instanciate all the nodes in a VPC inside AWS infrastructure.
The EPC nodes are simulated with the software developed in [this](https://github.com/networkedsystemsIITB/NFV_LTE_EPC) repository.

Version 1.0


## Prerequisites ##

You will need a Cloudify Manager running in AWS.

If you have not already, you can set up the [Cloudify environment](https://github.com/cloudify-examples/cloudify-environment-setup).
Installing that blueprint and following all of the configuration instructions will ensure you have all of the prerequisites, including keys, plugins, and secrets.

Otherwise, you may use an already configured [image](http://docs.getcloudify.org/4.0.0/installation/bootstrapping/#option-1-installing-a-cloudify-manager-image) provided by AWS.
These images include pre-installation of all dependencies and Cloudify Manager itself.


## Installation ##

* Dependencies for Cloudify Manager Premium image (ami-e3f0c985). You should install the following packages:
	> sudo yum install gcc libffi-devel python-devel openssl-devel

* Once you have a Cloudify Manager running in AWS, you can deploy the blueprint with the appropriate inputs. There is an input example file in scripts/vepc_inputs.yaml, which you can use to fill with your data and to add/delete inputs. You can also create your own inputs file.

* To install and deploy the blueprint, exec the following command in the project folder (with the Manager running):
	> cfy install -b vepc -i inputs/vepc_inputs.yaml  vepc_blueprint.yaml

* To experiment with data and control traffic over the vEPC, you can connect to the deployed RAN and SINK nodes from the Manager machine:
	> ssh -i "vepc-key.pem" ubuntu@ran_ip

	You can get the IP addresses of these nodes by executing:
		> cfy deployments outputs vepc

	That way you will also get the IP addresses of the MME and P-GW nodes, that you will need to run the code in RAN and SINK.


## Authors ##

1. [Moisés Pacheco Lorenzo](https://www.linkedin.com/in/mois%C3%A9s-rub%C3%A9n-pacheco-lorenzo-21b24113a/), Bachelor's student (2013-2017), Escola de Enxeñaría de Telecomunicación, Universidade de Vigo.
2. [Manuel Fernández Veiga](https://labredes.det.uvigo.es/node/207), Assistant Professor, Escola de Enxeñaría de Telecomunicación, Universidade de Vigo.
3. [Sadagopan N S](https://www.linkedin.com/in/sadagopan-n-s-b8184a61), Master's student (2014-2016), Dept. of Computer Science and Engineering, IIT Bombay.
4. [Prof. Mythili Vutukuru](https://www.cse.iitb.ac.in/~mythili/), Dept. of Computer Science and Engineering, IIT Bombay.
