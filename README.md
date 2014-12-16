PCF_AWS_CloudFormation
======================

Setup:
1. Ensure a bosh keypair doesn't already exist
2. Create a keypair (opsmgr would be good - but doesn't have to be)
3. Go to AWS CloudFormation and "Create" a new stack using the .json file in this repo

Use this file to:

1.  Create VPC
2.  Define Security Group
3.  Create NATS VPC Instance
4.  Create Subnets (pubic and private)
5.  Create Internet Gateway
6.  Create Route Tables
7.  Launch OpsManager Instance (using Pivotal AMI)
8.  

What's not working:
1.  Unable to get Security Group Name into CloudFormation script - it only gets the Group ID - This causes OpsManager to not find the Security group.  You can manually paste in the value
2.  The Final Step to automatically install "Director" doesn't work.  It will return an "Id" indicating success, but doesn't

To do:
1.  Wget Elastic Runtime (provide prompt with URL)
2.  Import Elastic Runtime into ops manager
3.  Extend Microbosh manifest to support a "warm" S3 cache with compile objects (this would reduce installation by 90 minutes)

