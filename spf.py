import numpy as np
import queue
import copy
import matplotlib.pyplot as plt


def minIndex(q, sortedIndex):
    min_index = -1
    min_val = 999999999999
    n = q.qsize()
    min_val = q.queue[0]
    for i in range(n):
        curr = q.queue[0]
        q.get()  # This is dequeue() in C++ STL

        # we add the condition i <= sortedIndex
        # because we don't want to traverse
        # on the sorted part of the queue,
        # which is the right part.
        if (ST[curr] <= ST[min_val] and i <= sortedIndex):
            min_index = i
            min_val = curr
        q.put(curr)  # This is enqueue() in
        # C++ STL
    return min_index


# Moves given minimum element to
# rear of queue
def insertMinToRear(q, min_index):
    min_val = None
    n = q.qsize()
    for i in range(n):
        curr = q.queue[0]
        q.get()
        if (i != min_index):
            q.put(curr)
        else:
            min_val = curr
    q.put(min_val)


def sortQueue(q):
    for i in range(1, q.qsize() + 1):
        min_index = minIndex(q, q.qsize() - i)
        insertMinToRear(q, min_index)

total_time = 10
IAT_rate = 50
ST_rate = 70
rho = IAT_rate / ST_rate

# Initialize Parameters
qu = queue.Queue()
curr_process = None
IAT = []
ST = []
AT = []
wait_time = []
wait_timeSPF = []
server_busy = False
list_wait = []
list_delay = []

num_processes = int(np.random.poisson(IAT_rate) * total_time)
print("Num process: %s", num_processes)
num_processes_served = 0

# Populate Inter-Arrival-Times (IAT)
print("INTER_ARIVAL")
for i in range(num_processes):
    temp = np.random.exponential(1 / IAT_rate) * 60 * 60
    print("IAT: %s", temp)
    if i == 0:
        IAT.append(0)
    else:
        print(int(temp - temp % 1))
        IAT.append(int(temp - temp % 1))

print("POPULATE SERVICE")
# Populate Service-Times (ST) (where ST[i]!=0)
while not len(ST) == num_processes:
    temp = np.random.exponential(1 / ST_rate) * 60 * 60
    print("ST: %s", temp)
    if not int(temp - temp % 1) < 1:
        print(int(temp - temp % 1))
        ST.append(int(temp - temp % 1))

# Save a copy of ST
ST_copy = copy.deepcopy(ST)

# Get Arrival-Times (AT) from IAT starting at t=0
# and initialize Waiting-Times to 0
for i in range(num_processes):
    if i == 0:
        AT.append(0)
    else:
        print("AT: %s", AT[i - 1] + IAT[i])
        AT.append(AT[i - 1] + IAT[i])
    wait_time.append(0)
    wait_timeSPF.append(0)


# Simulation of M/M/1 Queue (i represents current time)

for i in range(total_time * 60 * 60):
    if server_busy:
        # print("List:")
        for item in list(qu.queue):
            # print(ST[item])
            wait_timeSPF[item] = wait_timeSPF[item] + 1
        ST[curr_process] = ST[curr_process] - 1
        if ST[curr_process] == 0:
            server_busy = False
            num_processes_served = num_processes_served + 1

    for j in range(num_processes):
        if i == AT[j]:
            qu.put(j)
            sortQueue(qu)

    if not server_busy and not qu.empty():
        curr_process = qu.get()
        print("Curr:", ST[curr_process])
        server_busy = True

    sum_wait = 0
    sum_delay = 0

    for i in range(num_processes_served):
        sum_wait = sum_wait + wait_timeSPF[i]
        sum_delay = sum_delay + wait_timeSPF[i] + ST_copy[i]

    if num_processes_served == 0:
        list_wait.append(0)
        list_delay.append(0)
    else:
        list_wait.append(sum_wait / (num_processes_served * 60 * 60))
        list_delay.append(sum_delay / (num_processes_served * 60 * 60))

plt.plot([i + 1 for i in range(total_time * 60 * 60)], list_wait)
plt.ylabel("Avg Wait Times SPF")
plt.show()

plt.plot([i + 1 for i in range(total_time * 60 * 60)], list_delay)
plt.ylabel("Avg Delay Times SPF")
plt.show()

ST = copy.deepcopy(ST_copy)
server_busy = False
list_wait = []
list_delay = []
qu = queue.Queue()
curr_process = None

sum_wait = 0
sum_delay = 0
num_processes_served = 0

for i in range(total_time * 60 * 60):
    if server_busy:
        for item in list(qu.queue):
            wait_time[item] = wait_time[item] + 1
        ST[curr_process] = ST[curr_process] - 1
        if ST[curr_process] == 0:
            server_busy = False
            num_processes_served = num_processes_served + 1

    for j in range(num_processes):
        if i == AT[j]:
            qu.put(j)

    if not server_busy and not qu.empty():
        curr_process = qu.get()
        server_busy = True

    sum_wait = 0
    sum_delay = 0

    for i in range(num_processes_served):
        sum_wait = sum_wait + wait_time[i]
        sum_delay = sum_delay + wait_time[i] + ST_copy[i]

    if num_processes_served == 0:
        list_wait.append(0)
        list_delay.append(0)
    else:
        list_wait.append(sum_wait / (num_processes_served * 60 * 60))
        list_delay.append(sum_delay / (num_processes_served * 60 * 60))

plt.plot([i + 1 for i in range(total_time * 60 * 60)], list_wait)
plt.ylabel("Avg Wait Times FIFO")
plt.show()

plt.plot([i + 1 for i in range(total_time * 60 * 60)], list_delay)
plt.ylabel("Avg Delay Times FIFO")
plt.show()