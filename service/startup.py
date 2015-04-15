import os,time
import boto

def startinstance(instanceid):
 conn.start_instances(instance_ids=[instanceid])
 time.sleep(2)
 instancefound = "false"
 while (instancefound == "false"):
  if checkinstance(instanceid) <> "started":
   print "sleeping..."
   time.sleep(2)
  else:
   instancefound = "true"


def stopinstance(instanceid):
 conn.stop_instances(instance_ids=[instanceid])
 time.sleep(2)
 instancefound = "false"
 while (instancefound == "false"):
  if checkinstance(instanceid) <> "stopped":
   print "sleeping..."
   time.sleep(2)
  else:
   instancefound = "true"
 

def checkinstance(instanceid):
 res2=conn.get_all_instances()
 for rese in res2:
   for inst in rese.instances:
    if inst.id == instanceid:
     return inst.state
 return "error"

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

numinstance = 0

for res in reservations:
    for inst in res.instances:
            if inst.state == "running":
             instanceid.append(inst.id)
             instancename.append(inst.tags['Name'])
             numinstance = numinstance + 1

stoplist = []
for x in range(bootinstances - 1, -1,-1):
     for y in range (0,numinstance):
      if instancename[y].find(bootorder[x]) <> -1:
       print "Found It --> " + instancename[y] + " with " + bootorder[x]
       print "gonna check instance-> " + instanceid[y]
       if checkinstance(instanceid[y]) == "running":
        stopinstance(instanceid[y])
       break;


