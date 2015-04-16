#Service Manager



This utility is used to help stop/start PCF installations on AWS.  In this example, it assumes you have your AWS Access Key and AWS secret key configured in a file located in ~/ called .boto


contents of ~/.boto file

**[Credentials]**

aws_access_key_id = <Your Access Key ID>

aws_secret_access_key = <Your AWS Secret ID>


##Required:
####1.  boto  (pip install boto)
####2.  python (I have version 2.7.x)


###Syntax:
```sh
python service.py [stop/start] [vpc_id]
```

###example:

```sh
$ python service.py start vpc-fbc79c9e
```
