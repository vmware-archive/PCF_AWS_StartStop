import sys,os,time
import boto.ec2, boto.ec2.elb
from boto.exception import EC2ResponseError

option1 = sys.argv[1]
vpc_id = sys.argv[2]

argv_len = len(sys.argv)

## This assumes if no region is listed it is the default aws_region of us-east-1
if argv_len == 3:
 aws_region = "us-east-1"

if argv_len == 4:
 aws_region = sys.argv[3]


routerinstances = []

print option1 + ": vpc_id=" + vpc_id + " within aws_region: " + aws_region

def startinstance(instanceid):
 conn.start_instances(instance_ids=[instanceid])

def stopinstance(instanceid):
 conn.stop_instances(instance_ids=[instanceid])
 
def checkinstance(instanceid):
  try:
   res=conn.get_all_instances(instance_ids=[instanceid])

   for res in res:
     for inst in res.instances:
      if inst.id == instanceid:
       return inst.state
  except EC2ResponseError:
    return "error"

def getpublicdns(instanceid):
  try:
   res=conn.get_all_instances(instance_ids=[instanceid])
   for res in res:
     for inst in res.instances:
      if inst.id == instanceid:
       return inst.public_dns_name
  except EC2ResponseError,e:
      print e    
  return "error" 

def do_task():
  time.sleep(1)

def example_1(n):
  for i in range(n):
    do_task()
    print '\b.',
    sys.stdout.flush()
  print ' Done!'
  

def shutdown():
 numinstance = 0
 for res in reservations:
     for inst in res.instances:
            if (inst.state == "running" and inst.vpc_id == vpc_id):
             instanceid.append(inst.id)
             instancename.append(inst.tags['Name'])
             print "Adding instancename for shutdown:" + inst.tags['Name'] + " : " + inst.id 
             if 'Name' in inst.tags:
               if inst.tags['Name'].find("microbosh") <> -1:
                microboshinstance = numinstance
               numinstance = numinstance + 1

 print "Total number of instances for shutdown:" , numinstance
 ## Microbosh should be shutdown first or you'll have things likely ressurected!
 print "Stopping Microbosh"
 stopinstance(instanceid[microboshinstance])
 
 for y in range (0,numinstance):
 	for x in range(bootinstances - 1, -1,-1):
	   if instancename[y].find(bootorder[x]) <> -1:
	    if checkinstance(instanceid[y]) == "running":
	     print "Stopping Instance: " + instanceid[y] + " : " + instancename[y]
	     stopinstance(instanceid[y])
	    break;
 print "Shutdown Complete!"       





def startup():
 numinstance = 0
 OpsManagerInstanceId=None
 for res in reservations:
     for inst in res.instances:
            if (inst.state == "stopped" and inst.vpc_id == vpc_id):
             instanceid.append(inst.id)
             instName = inst.tags['Name']
             instancename.append(instName)
             print "Added instancename:instanceid: ", instName + " : " + inst.id 
             if inst.tags['Name'].find("microbosh") <> -1:
              microboshinstance = numinstance
             if inst.tags['Name'].find("Ops Manager") <> -1:
              OpsManagerInstanceId = inst.id
             if inst.tags['Name'].find("router") <> -1:
              print "Found a router - marking for ELB Addition..."
              routerinstance = numinstance
              routerinstances.append(inst.id) 
             numinstance = numinstance + 1

 for y in range (0,numinstance):
      for x in range(bootinstances - 1, -1,-1):
       if instancename[y].find(bootorder[x]) <> -1:
        if checkinstance(instanceid[y]) == "stopped":
         print "Starting Instance: " + instanceid[y] + " : " + instancename[y]
         startinstance(instanceid[y])
        break;
  
 print "Starting Microbosh"
 startinstance(instanceid[microboshinstance])

 ## Since the Router has restarted we need to Remove and Add the router to the existing ELB.
 elbconn = boto.ec2.elb.connect_to_region(aws_region)

 ## This section assigns the elb that has a matching vpc_id
 load_balancers = elbconn.get_all_load_balancers()
 for elb in load_balancers:
  if elb.vpc_id == vpc_id:
   load_balancer = elb
 elbrouterinstances = load_balancer.instances
 print "Here's a list of routers: " + str(routerinstances)
 for inst in elbrouterinstances:
  print "Removing instance: " + str(inst.id) + " from ELB: " + load_balancer.name
  elbconn.deregister_instances(load_balancer.name,inst.id)
 
 print "Waiting for router to startup..."
 print "routerinstances:", routerinstances

 for inst in routerinstances:
  instanceready = "false"
  while (instanceready == "false"):
   if checkinstance(inst) <> "running":
    time.sleep(5)
   else:
    instanceready = "true"

 ## This appears to be a reasonable amount of time for the services within the VM to startup.  
 ## Since this VM is in a private subnet inaccessible from internet there's no way to test for specific service startup
 ## If added to early the ELB views the instance as "unhealthy" and marks it out of service
 ## Another way to potentially check on this would be to check the state of the ELB instance (i.e. InService or OutOfService) and remove/add with delay until InService

 print 'Waiting ',
 example_1(130)



 for inst in routerinstances:
  print "Adding instance: " + inst + " to ELB: " + load_balancer.name
  elbconn.register_instances(load_balancer.name,inst)
 print "Startup Complete!"
 print "Ops Manager Public DNS: http://" + getpublicdns(OpsManagerInstanceId)

conn = boto.ec2.connect_to_region(aws_region)
reservations = conn.get_all_instances()

instanceid = []
instancename = []

bootorder = 'bootorder.txt'
with open(bootorder, "r") as boot:
  bootorder = []
  bootinstances = 0
  for line in boot:
    bootinstances = bootinstances + 1
    line = line.rstrip('\n')
    bootorder.append(line)


if option1 == "start":
 print "heading to startup"
 startup();
if option1 == "stop":
 print "heading to shutdown"
 shutdown();
