import sys,os,time
import boto

option1 = sys.argv[1]
vpc_id = sys.argv[2]

print option1 + ": vpc_id=" + vpc_id

def startinstance(instanceid):
 conn.start_instances(instance_ids=[instanceid])
 time.sleep(2)
 instancefound = "false"
 while (instancefound == "false"):
  if checkinstance(instanceid) <> "running":
   print "sleeping..."
   time.sleep(15)
  else:
   instancefound = "true"


def stopinstance(instanceid):
 conn.stop_instances(instance_ids=[instanceid])
 time.sleep(2)
 instancefound = "false"
 while (instancefound == "false"):
  if checkinstance(instanceid) <> "stopped":
   print "sleeping..."
   time.sleep(15)
  else:
   instancefound = "true"
 

def checkinstance(instanceid):
 res=conn.get_all_instances()
 for res in res:
   for inst in res.instances:
    if inst.id == instanceid:
     return inst.state
 return "error"

def shutdown():
 numinstance = 0
 for res in reservations:
     for inst in res.instances:
            if (inst.state == "running" and inst.vpc_id == vpc_id):
             instanceid.append(inst.id)
             instancename.append(inst.tags['Name'])
             if inst.tags['Name'].find("microbosh") <> -1:
              microboshinstance = numinstance
              #print "microbosh is-->" + instancename[microboshinstance]
             numinstance = numinstance + 1

 ## Microbosh should be shutdown first or you'll have things likely ressurected!
 print "Stopping Microbosh"
 stopinstance(instanceid[microboshinstance])
 
 for x in range(bootinstances - 1, -1,-1):
      for y in range (0,numinstance):
       if instancename[y].find(bootorder[x]) <> -1:
        #print "Found It --> " + instancename[y] + " with " + bootorder[x]
        #print "gonna check instance-> " + instanceid[y]
        if checkinstance(instanceid[y]) == "running":
         print "Stopping Instance: " + instanceid[y] + " : " + instancename[y]
         stopinstance(instanceid[y])
        break;
        
def startup():
 numinstance = 0
 for res in reservations:
     for inst in res.instances:
            if (inst.state == "stopped" and inst.vpc_id == vpc_id):
             instanceid.append(inst.id)
             instancename.append(inst.tags['Name'])
             if inst.tags['Name'].find("microbosh") <> -1:
              microboshinstance = numinstance
              #print "microbosh is-->" + instancename[microboshinstance]
             numinstance = numinstance + 1

 for x in range(bootinstances - 1, -1,-1):
      for y in range (0,numinstance):
       if instancename[y].find(bootorder[x]) <> -1:
        #print "Found It --> " + instancename[y] + " with " + bootorder[x]
        #print "gonna check instance-> " + instanceid[y]
        if checkinstance(instanceid[y]) == "stopped":
         print "Starting Instance: " + instanceid[y] + " : " + instancename[y]
         startinstance(instanceid[y])
        break;
  
 print "Starting Microbosh"
 startinstance(instanceid[microboshinstance])


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

