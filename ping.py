import subprocess
import threading
from multiprocessing import JoinableQueue

import time

import os


class PingService:

    def __init__(self, ipMap):
        self.onlineQueue = JoinableQueue()
        self.ipMap = ipMap

    def startPing(self):
        hosts = self.ipMap.values()
        for host in hosts:
            threading.Thread(target=self.ping, args=(host,)).start()

    def ping(self, host):
        if os.name == 'nt':
            # Configure subprocess to hide the console window
            info = subprocess.STARTUPINFO()
            info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = subprocess.SW_HIDE

            output = subprocess.Popen(['ping', '-n', '2', '-w', '500', str(host)], stdout=subprocess.PIPE,
                                      startupinfo=info).communicate()[0]

            if "Destination host unreachable" not in output.decode('utf-8') \
                    and "Request timed out" not in output.decode('utf-8'):
                self.onlineQueue.put(host)
        else:
            output = subprocess.Popen(['ping', '-c', '2', '-W', '1', str(host)],
                                      stdout=subprocess.PIPE).communicate()[0]

            if "Destination host unreachable" not in output.decode('utf-8') \
                    and "Request timed out" not in output.decode('utf-8') \
                    and "100% packet loss" not in output.decode('utf-8'):
                self.onlineQueue.put(host)

    def pingAndParseResult(self, onlineMap):
        threading.Thread(target=self.startPing).start()
        while not self.onlineQueue.empty():
            host = self.onlineQueue.get()
            onlineMap[list(self.ipMap.keys())[list(self.ipMap.values()).index(host)]] = time.time()
        return onlineMap


if __name__ == '__main__':
    print("Running app")
    onlineMap = {}
    ipMap = {
        "KG": "192.168.1.84",
        "OG": "192.168.1.126",
        "SG": "192.168.1.153",
        "HH": "192.168.1.124",
        "OF": "192.168.1.161"
    }
    pinger = PingService(ipMap)

    onlineMap = pinger.pingAndParseResult(onlineMap)
    #time.sleep(5)
    print(onlineMap)
    onlineMap = pinger.pingAndParseResult(onlineMap)
    time.sleep(5)
    print(onlineMap)
    onlineMap = pinger.pingAndParseResult(onlineMap)
    time.sleep(5)
    print(onlineMap)
    onlineMap = pinger.pingAndParseResult(onlineMap)
    time.sleep(5)
    onlineMap = pinger.pingAndParseResult(onlineMap)
    print(onlineMap)
