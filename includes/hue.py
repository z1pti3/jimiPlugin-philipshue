import requests
import json
import time
from datetime import datetime

class hue():
    apiAddress = str()
    user = str()

    def __init__(self,apiAddress,user):
        self.apiAddress = apiAddress
        self.user = user

    def registerUser(self):
        data = json.dumps({"devicetype":"jimi"})
        response = requests.post(self.apiAddress, data=data)
        responseJson = json.loads(response.text)[0]
        if "error" in responseJson:
            # 101 = link button not pressed
            return responseJson["error"]["type"], None
        elif "success" in responseJson:
            return 200, responseJson["success"]["username"]
        return None, None

    def getSensors(self):
        apiCall = "{0}/{1}/{2}".format(self.apiAddress,self.user,"sensors")
        response = requests.get(apiCall)
        responseJson = json.loads(response.text)
        if "error" in responseJson:
            return None
        result = {}
        resultsTemp = {}
        for key, value in responseJson.items():
            value["id"] = key
            if "uniqueid" in value:
                if value["uniqueid"].split("-")[0] not in resultsTemp:
                    resultsTemp[value["uniqueid"].split("-")[0]] = {}
                resultsTemp[value["uniqueid"].split("-")[0]][value["type"]] = value
            else:
                result[value["name"]] = value
        for key, value in resultsTemp.items():
            for itemKey, itemValue in value.items():
                if itemValue["uniqueid"].split("-")[-1] == "0406":
                    result[itemValue["name"]] = value
                    break
        return result

    def refreshSensor(self,sensor,sensorType=None):
        if not sensorType:
            for sensorKey, sensorItem in sensor.items():
                apiCall = "{0}/{1}/{2}/{3}".format(self.apiAddress,self.user,"sensors",sensorItem["id"])
                response = requests.get(apiCall)
                responseJson = json.loads(response.text)
                responseJson["id"] = sensorItem["id"]
                sensor[sensorKey] = responseJson
        else:
            apiCall = "{0}/{1}/{2}/{3}".format(self.apiAddress,self.user,"sensors",sensor[sensorType]["id"])
            response = requests.get(apiCall)
            responseJson = json.loads(response.text)
            responseJson["id"] = sensor[sensorType]["id"]
            sensor[sensorType] = responseJson
        return sensor

    def sensorMotion(self,sensor,pause=1,autoUpdate=True):
        if autoUpdate:
            self.refreshSensor(sensor,"ZLLPresence")
        if "ZLLPresence" in sensor:
            # checking for presence
            d = datetime.utcnow()
            epoch = datetime(1970,1,1)
            now = (d - epoch).total_seconds()
            lastUpdated = datetime.strptime(sensor["ZLLPresence"]["state"]["lastupdated"], '%Y-%m-%dT%H:%M:%S').timestamp()
            if (sensor["ZLLPresence"]["state"]["presence"] or ( lastUpdated + ( pause * 60 ) ) > now ):
                return True
        return False

    def sensorTemperature(self,sensor,autoUpdate=True):
        if autoUpdate:
            self.refreshSensor(sensor,"ZLLTemperature")
        if "ZLLTemperature" in sensor:
            return sensor["ZLLTemperature"]["state"]["temperature"] / 100
        return None

    def sensorLight(self,sensor,autoUpdate=True):
        if autoUpdate:
            self.refreshSensor(sensor,"ZLLLightLevel")
        if "ZLLLightLevel" in sensor:
            return sensor["ZLLLightLevel"]["state"]["lightlevel"]
        return None

    def getNames(self,resultDict):
        result = []
        for key, value in resultDict.items():
            result.append(key)
        return result

    def getGroups(self):
        apiCall = "{0}/{1}/{2}".format(self.apiAddress,self.user,"groups")
        response = requests.get(apiCall)
        responseJson = json.loads(response.text)
        if "error" in responseJson:
            return None
        result = {}
        for key, value in responseJson.items():
            value["id"] = key
            result[value["name"]] = value
        return result

    def groupOn(self,group):
        apiCall = "{0}/{1}/{2}/{3}/action".format(self.apiAddress,self.user,"groups",group["id"])
        data = json.dumps({"on":True})
        response = requests.put(apiCall, data=data)
        responseJson = json.loads(response.text)[0]
        if "success" in responseJson:
            if responseJson["success"]["/groups/{0}/action/on".format(group["id"])] == True:
                return True
        return False

    def groupOff(self,group):
        apiCall = "{0}/{1}/{2}/{3}/action".format(self.apiAddress,self.user,"groups",group["id"])
        data = json.dumps({"on":False})
        response = requests.put(apiCall, data=data)
        responseJson = json.loads(response.text)[0]
        if "success" in responseJson:
            if responseJson["success"]["/groups/{0}/action/on".format(group["id"])] == False:
                return True
        return False

    def getLights(self):
        apiCall = "{0}/{1}/{2}".format(self.apiAddress,self.user,"lights")
        response = requests.get(apiCall)
        responseJson = json.loads(response.text)
        if "error" in responseJson:
            return None
        result = {}
        for key, value in responseJson.items():
            value["id"] = key
            result[value["name"]] = value
        return result

    def lightOn(self,light):
        apiCall = "{0}/{1}/{2}/{3}/state".format(self.apiAddress,self.user,"lights",light["id"])
        data = json.dumps({"on":True})
        response = requests.put(apiCall, data=data)
        responseJson = json.loads(response.text)[0]
        if "success" in responseJson:
            if responseJson["success"]["/lights/{0}/state/on".format(light["id"])] == True:
                return True
        return False

    def lightOff(self,light):
        apiCall = "{0}/{1}/{2}/{3}/state".format(self.apiAddress,self.user,"lights",light["id"])
        data = json.dumps({"on":False})
        response = requests.put(apiCall, data=data)
        responseJson = json.loads(response.text)[0]
        if "success" in responseJson:
            if responseJson["success"]["/lights/{0}/state/on".format(light["id"])] == False:
                return True
        return False

    def refreshLight(self,light):
        apiCall = "{0}/{1}/{2}/{3}".format(self.apiAddress,self.user,"lights",light["id"])
        response = requests.get(apiCall)
        responseJson = json.loads(response.text)
        responseJson["id"] = light["id"]
        light = responseJson
        return light

    def lightsFlash(self,light,count,delay=0.75):
        currentState = light["state"]["on"]
        if currentState:
            self.lightOff(light)
            time.sleep(delay)
        for i in range(0,count-1):
            self.lightOn(light)
            time.sleep(delay)
            self.lightOff(light)
            time.sleep(delay)
        if currentState:
            self.lightOn(light)
