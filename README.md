#Service Manager



This utility is used to help stop/start PCF installations on AWS.  In this example, it assumes you have your AWS Access Key and AWS secret key configured in a file located in ~/ called .boto


contents of ~/.boto file

```
[Credentials]
aws_access_key_id = <Your Access Key ID>
aws_secret_access_key = <Your AWS Secret ID>
```

If you followed the [documented process] (http://cf-p1-docs-acceptance.cfapps.io/pivotalcf/customizing/pcf-aws-component-config.html) to create your AWS PCF environment, there are two things you need to do to make this utility work:

1. Make sure that the IAM user associated with the access key has sufficient permissions to start and stop vms. By default it does not, and the script will fail with a message saying ```boto.exception.EC2ResponseError: EC2ResponseError: 403 Forbidden```. The quickest way to assign the needed permissions is to go in to AWS IAM and attach the AmazonEC2FullAccess managed policy to the user. The better, more secure, way is to add the following statement to the inline policy for the user:
  
  ```
          {
              "Sid": "StopStart",
              "Effect": "Allow",
              "Action": [
                  "ec2:StopInstances",
                  "ec2:StartInstances"
              ],
              "Resource": "*"
          }
  ```

2. Make sure that your EC2 instance names match the names in the bootorder.txt file. By default, the Ops Manager and NAT instances are left unnamed. The bootorder.txt file, and the service.py script, expect them to be "Ops Manager" and "Nat1", respectively. Using a different name for the Ops Manager instance requires a change in both places. And case matters.


##Required:
####1.  boto  (pip install boto)
####2.  python (I have version 2.7.x)


###Syntax:
```sh
python service.py [stop/start/elb] [vpc_id] [aws-region (default if left blank is "us-east-1")]
```

###example:

```sh

$ python service.py start vpc-fbc79c9e
```
OR Optionally specify aws_region (default is "us-east-1")
```sh
$ python service.py start vpc-fbc79c9e us-east-1
```

The `elb` option will just update Elastic Load Balancer instances to the current Diego Brain and Router instances.  It is automatically run as part of the `start` option.


###Things to watch for
1. If Ops Manager is not being started. Check in AWS console that Ops Manager instance Tag name is 'Ops Manager' and not 'OpsManager'
