import subprocess
from multiprocessing import JoinableQueue

import time


def ping(hosts, queue):

    # Configure subprocess to hide the console window
    #info = subprocess.STARTUPINFO
    #info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #info.wShowWindow = subprocess.SW_HIDE

    for i in range(len(hosts)):
        output = subprocess.Popen(['ping', '-W', '200', str(hosts[i])], stdout=subprocess.PIPE).communicate()[0]

        print(output.decode('utf-8'))

        if "Destination host unreachable" not in output.decode('utf-8') \
                and "Request timed out" not in output.decode('utf-8'):

            queue.put(hosts[i])


def pingAndParseResult(ipMap, onlineMap):
    onlineQueue = JoinableQueue()
    ping(list(ipMap.values()), onlineQueue)
    while not onlineQueue.empty():
        host = onlineQueue.get()
        onlineMap[list(ipMap.keys())[list(ipMap.values()).index(host)]] = time.time()
    return onlineMap
