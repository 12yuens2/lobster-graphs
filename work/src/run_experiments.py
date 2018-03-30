import os
import subprocess
import sys
import random

import numpy as np

FNULL = open(os.devnull, "w")

def get_active_hosts():
    hosts = ["pc3-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,70)]
    #hosts += ["pc2-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(30,99)]
    #hosts += ["pc2-"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(100,150)]


    print("Pinging hosts...")
    activehosts = []
    for hostname in hosts:
        print("Pinging " + hostname)
        try:
            process1 = subprocess.run(["ping", "-c", "1", "-w", "1", hostname], stdout=FNULL)
            process2 = subprocess.run(["ssh", hostname, "pwd"], stdout=FNULL, timeout=1)

            if process1.returncode == 0 and process2.returncode == 0:
                activehosts.append(hostname)

        except subprocess.TimeoutExpired:
            print(hostname + " timed out")
            
    print("Active hosts: " + str(len(activehosts)))

    random.shuffle(activehosts)

    return activehosts


def ssh_process(hostname, label_threshold, histogram_threshold):
    return ["ssh", hostname, "cd ~/Documents/cs4099/work/src && source ../env/bin/activate && python combination.py " + str(label_threshold) + " " + str(histogram_threshold)]


activehosts = get_active_hosts()

processes = {}
i = 0 
for label_threshold in np.arange(0.03, 0.1, 0.01):
    for hist_threshold in np.arange(0.3, 1, 0.1):
        print("Running experiment on " + activehosts[i])
        p = subprocess.Popen(ssh_process(activehosts[i], label_threshold, hist_threshold), stdout=FNULL)
        processes[activehosts[i],label_threshold,hist_threshold] = p

        i += 1


for k,v in processes.items():
    try:
        processes[k] = v.wait(timeout=18000) # timeout = 5hours
    except subprocess.TimeoutExpired:
        processes[k] = 1


for ((hostname,label_threshold,hist_threshold),v) in processes.items():
    if v == 0:
        print(hostname + " completed with label_threshold:" + str(label_threshold) + " and hist_threshold:" + str(hist_threshold))
    else:
        print(hostname + " failed to complete with label_threshold:" + str(label_threshold) + " and hist_threshold:" + str(hist_threshold))
         
