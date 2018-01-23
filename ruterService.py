import urllib.request
import json
import threading
import time
from multiprocessing import JoinableQueue
from datetime import datetime, timezone
from dateutil import parser

url = 'http://reisapi.ruter.no/StopVisit/GetDepartures/3010521?linenames=21'

class RuterService:

    def __init__(self, routeId, stopId, direction):
        self.routeId = routeId
        self.stopId = stopId
        self.direction = direction
        self.updateQueue = JoinableQueue()
        self.cached_response = None
        self.stopName = None
        self.destName = None

    def requestStopName(self):
        url = 'http://reisapi.ruter.no/Place/GetStop/' + str(self.stopId)
        with urllib.request.urlopen(url) as response:
            r = response.read()
            if (r == None):
                print("ResponseBody is empty")
                return
            else:
                res = json.loads(r.decode('utf-8'))
        self.stopName = res['Name']

    def getStopName(self):
        if(self.stopName == None):
            threading.Thread(target=self.requestStopName).start()
            return '-'
        else:
            return self.formatName(self.stopName)

    def getDestName(self):
        if(self.destName == None):
            return '-'
        else:
            return self.formatName(self.destName)

    def formatName(self, name):
        if '(' in name:
            name = name[:name.find('(')]
        if '[' in name:
            name = name[:name.find('[')]
        return name.upper()

    def getDeparturesResponse(self):
        url = 'http://reisapi.ruter.no/StopVisit/GetDepartures/' \
              + str(self.stopId) + \
              '?linenames=' + str(self.routeId)
        with urllib.request.urlopen(url) as response:
            r = response.read()
            if (r == None):
                print("ResponseBody is empty")
                return
            else:
                res = json.loads(r.decode('utf-8'))
        self.updateQueue.put(res)

    def refresh(self):
        threading.Thread(target=self.getDeparturesResponse).start()

    def update_cache(self):
        while not self.updateQueue.empty():
            self.cached_response = self.updateQueue.get()

    def getDepartures(self):
        self.update_cache()
        if self.cached_response == None:
            return []
        departureTimes = []
        for item in self.cached_response:
            if item['MonitoredVehicleJourney']['DirectionName'] == self.direction:
                if (self.destName == None):
                    self.destName = item['MonitoredVehicleJourney']['DestinationName'].upper()
                departureTimes.append(item['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime'])
        return departureTimes

    def getNextDepartures(self, maxNumber):
        departureTimes = self.getDepartures()
        if departureTimes.__sizeof__() > maxNumber:
            return departureTimes[0:maxNumber]
        return departureTimes

    def getNextDeparturesInText(self, maxNumber):
        departuresInStrings = []
        for dep in self.getNextDepartures(maxNumber):
            dt = parser.parse(dep)
            delta = dt - datetime.now(timezone.utc)
            deltaMin = int(delta.seconds / 60)
            if (deltaMin < 1):
                departuresInStrings.append('now')
            elif (deltaMin < 20):
                departuresInStrings.append(str(deltaMin) + ' min')
            else:
                departuresInStrings.append(str(dt.hour).zfill(2) + ':' + str(dt.minute).zfill(2))

        return departuresInStrings




if __name__ == '__main__':
    print("Running app")

    ##parsing response
    counter = 0

    depService = RuterService('13', '3010520', '1')
    depService.refresh()
    print(depService.getNextDeparturesInText(5))
    depService.update_cache()
    #time.sleep(5)
    print(depService.getNextDeparturesInText(5))
    depService.update_cache()
    time.sleep(1)
    print(depService.getNextDeparturesInText(5))
    depService.update_cache()
    time.sleep(1)
    print(depService.getNextDeparturesInText(5))
    depService.update_cache()
    time.sleep(1)
    depService.update_cache()
    print(depService.getNextDeparturesInText(5))


    ##parcing json