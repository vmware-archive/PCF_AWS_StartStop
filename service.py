import sys,os,time
import boto

option1 = sys.argv[1]
vpc_id = sys.argv[2]
routerinstances = []

print option1 + ": vpc_id=" + vpc_id

def startinstance(instanceid):
 conn.start_instances(instance_ids=[instanceid])

def stopinstance(instanceid):
 conn.stop_instances(instance_ids=[instanceid])
 
def checkinstance(instanceid):
 res=conn.get_all_instances()
 for res in res:
   for inst in res.instances:
    if inst.id == instanceid:
     return inst.state
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
             if inst.tags['Name'].find("microbosh") <> -1:
              microboshinstance = numinstance
             numinstance = numinstance + 1

 ## Microbosh should be shutdown first or you'll have things likely ressurected!
 print "Stopping Microbosh"
 stopinstance(instanceid[microboshinstance])
 
 for x in range(bootinstances - 1, -1,-1):
      for y in range (0,numinstance):
       if instancename[y].find(bootorder[x]) <> -1:
        if checkinstance(instanceid[y]) == "running":
         print "Stopping Instance: " + instanceid[y] + " : " + instancename[y]
         stopinstance(instanceid[y])
        break;
 print "Shutdown Complete!"       
def startup():
 numinstance = 0
 for res in reservations:
     for inst in res.instances:
            if (inst.state == "stopped" and inst.vpc_id == vpc_id):
             instanceid.append(inst.id)
             instancename.append(inst.tags['Name'])
             if inst.tags['Name'].find("microbosh") <> -1:
              microboshinstance = numinstance
             if inst.tags['Name'].find("router") <> -1:
              print "Found a router - marking for ELB Addition..."
              routerinstance = numinstance
              routerinstances.append(inst.id) 
             numinstance = numinstance + 1

 for x in range(bootinstances - 1, -1,-1):
      for y in range (0,numinstance):
       if instancename[y].find(bootorder[x]) <> -1:
        if checkinstance(instanceid[y]) == "stopped":
         print "Starting Instance: " + instanceid[y] + " : " + instancename[y]
         startinstance(instanceid[y])
        break;
  
 print "Starting Microbosh"
 startinstance(instanceid[microboshinstance])

 ## Since the Router has restarted we need to Remove and Add the router to the existing ELB.
 elbconn=boto.connect_elb()
 load_balancer = elbconn.get_all_load_balancers()[0]
 elbrouterinstances = load_balancer.instances
 print "Here's a list of routers: " + str(routerinstances)
 for inst in elbrouterinstances:
  print "Removing instance: " + str(inst.id) + " from ELB: " + load_balancer.name
  elbconn.deregister_instances(load_balancer.name,inst.id)
 print "Waiting for router to startup..."
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


 load_balancer = elbconn.get_all_load_balancers()[0]
 for inst in routerinstances:
  print "Adding instance: " + inst + " to ELB: " + load_balancer.name
  elbconn.register_instances(load_balancer.name,inst)
 print "Startup Complete!"

conn=boto.connect_ec2()
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
