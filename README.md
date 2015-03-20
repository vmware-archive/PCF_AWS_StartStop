PCF_AWS_CloudFormation
======================

Setup:


1. Create a keypair (opsmgr would be good - but doesn't have to be)
2. Add Key to your local mac (avoids having to do ssh -i <key> everytime you connect to AWS)
  $ ssh-add ~/.ssh/your-key.pem
3. Get your AWS KEY ID and SECRET KEY for your AWS account.
4. Go to AWS CloudFormation and "Create" a new stack using the .json file in this repo
5. Connect to your OpsManager Instance via Web/SSH
  $ ssh tempest@<PublicDNSNameOfOpsManagerInstance>


Use this file to:

1.  Create VPC
2.  Define Security Group
3.  Create NATS VPC Instance
4.  Create Subnets (pubic and private)
5.  Create Internet Gateway
6.  Create Route Tables
7.  Launch OpsManager Instance (using Pivotal AMI)
8.  Setup admin userid/password
9.  Import Elastic Runtime from specified URL

What's not working:

1.  The SSHKey Cloud Formation Parameter doesn't read well and place into the XML that gets imported into PCF


To do:
1.  Get SSHKey Parameter working!
2.  Add Elastic Runtime
3.  Configure Elastic Runtime
4.  Perform automated installation
