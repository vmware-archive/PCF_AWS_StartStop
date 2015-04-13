PCF_AWS_CloudFormation
======================

Setup:

1. Create a keypair (opsmgr would be good - but doesn't have to be)
2. Go to AWS CloudFormation and "Create" a new stack using the .json file in this repo
3. Give a name to the Elastic Load Balancer
4. Provide an (optional) URL to where Elastic Runtime can be downloaded and installed
5. Update any default values to desired
6. Click "Create"
7. In about 8-10 Minutes you'll have an Ops Manager up and running
8. In about 30-35 Munutes you'll have Ops Manager up and running with Elastic Runtime imported (if URL specified)
9. Use the "Outputs" Tab in the CloudFormation screen for items to copy/paste into OpsManager
10. Click "Apply Changes" and in ~2 Hours PCF Should be deployed


Use this file to:

1.  Create VPC
2.  Define Security Groups
   - Outbound Nat, ELB, PCF VMs, Ops Manager
3.  Create NATS VPC Instance
4.  Create Subnets (pubic and private)
5.  Create Internet Gateway
6.  Create Route Tables
7.  Create Elasticruntime and OpsManager S3 Buckets
7.  Create IAM User
    - Assign Elasticruntime and OpsManager S3 Bucket policy
8.  Create RDS Instance
9.  Create RDS Databases
10.  Create Acccess Key / Secret Key for IAM User
11.  .  Create Enterprise Load Balancer
12.  Launch OpsManager Instance (using Pivotal AMI)
13.  Setup admin userid/password
14.  Import Elastic Runtime from specified URL (optional)
