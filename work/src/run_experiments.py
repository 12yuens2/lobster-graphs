import os
import subprocess
import sys

import numpy as np

def get_active_hosts():
    hosts = ["pc3-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,70)]
    hosts += ["pc2-0"+str(host_id)+"-l.cs.st-andrews.ac.uk" for host_id in range(10,99)]

    print("Pinging hosts...")
    activehosts = []
    for hostname in hosts:
        process = subprocess.run(["ping", "-c", "1", "-w", "1", hostname], stdout=FNULL)
        if process.returncode == 0:
            activehosts.append(hostname)
            
    print("Active hosts: " + str(len(activehosts)))

    random.shuffle(activehosts)

    return activehosts


def ssh_process(hostname, label_threshold, histogram_threshold):
    return ["ssh", hostname, "cd ~/Documents/cs4099/work/src && source ../env/bin/activate && python combination.py " + str(label_threshold) + " " + str(histogram_threshold)]


activehosts = get_active_hosts()

label_threshold_range = np.arange(0.01, 0.2, 0.01)
hist_threshold_range = no.arange(0.1, 0.9, 0.1)

if len(activehosts) < len(label_threshold_range) + len(hist_threshold_range):
    print("Not enough machines for experiment")
    exit(1)

processes = {}
i = 0 
for label_threshold in np.arange(0.01, 0.2, 0.01):
    for hist_threshold in np.arange(0.1, 0.9, 0.1):
       p = subprocess.Popen(ssh_process(activehosts[i], label_threshold, hist_threshold))
       processes[activehosts[i],label_threshold,hist_threshold] = p

       i += 1


for k,v in processes.items():
    processes[k] = v.wait()


print("Finished...")
