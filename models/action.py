import requests
from pathlib import Path

from core.models import action
from core import helpers, cache

from plugins.philipshue.includes import hue

class _philipshueMotionDetected(action._action):
    apiAddress = str()
    user = str()
    sensorName = str()
    detectionPause = int()
    refreshSensor = bool()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        sensorName = helpers.evalString(self.sensorName,{"data" : data})

        hueApi = hue.hue(apiAddress,user)
        sensors = cache.globalCache.get("philipshueList","sensors",getPhilipshueList,apiAddress,user,dontCheck=self.refreshSensor)
        detectionPause = 1
        if self.detectionPause > 0:
            detectionPause = self.detectionPause
        motionDetected = hueApi.sensorMotion(sensors[sensorName],pause=detectionPause,autoUpdate=self.refreshSensor)

        actionResult["result"] = motionDetected
        actionResult["rc"] = 0
        return actionResult

class _philipshueGetSensors(action._action):
    apiAddress = str()
    user = str()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})

        sensors = cache.globalCache.get("philipshueList","sensors",getPhilipshueList,apiAddress,user,forceUpdate=True)

        actionResult["result"] = True
        actionResult["data"]["sensors"] = sensors
        actionResult["rc"] = 0
        return actionResult

class _philipshueGetSensor(action._action):
    apiAddress = str()
    user = str()
    sensorName = str()
    refreshSensor = bool()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")

    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        sensorName = helpers.evalString(self.sensorName,{"data" : data})

        sensors = cache.globalCache.get("philipshueList","sensors",getPhilipshueList,apiAddress,user,dontCheck=self.refreshSensor)
        if self.refreshSensor:
            hueApi = hue.hue(apiAddress,user)
            sensors[sensorName] = hueApi.refreshSensor(sensors[sensorName])

        actionResult["result"] = True
        actionResult["data"]["sensor"] = sensors[sensorName]
        actionResult["rc"] = 0
        return actionResult

class _philipshueLighThreshold(action._action):
    apiAddress = str()
    user = str()
    sensorName = str()
    minLightLevel = int()
    refreshSensor = bool()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")

    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        sensorName = helpers.evalString(self.sensorName,{"data" : data})

        minLightLevel = 0
        if self.minLightLevel > 0:
            minLightLevel = self.minLightLevel

        sensors = cache.globalCache.get("philipshueList","sensors",getPhilipshueList,apiAddress,user,dontCheck=self.refreshSensor)
        hueApi = hue.hue(apiAddress,user)
        lightlevel = hueApi.sensorLight(sensors[sensorName],autoUpdate=self.refreshSensor)

        if lightlevel > minLightLevel:
            actionResult["result"] = True
        else:
            actionResult["result"] = False
        actionResult["data"]["lightLevel"] = lightlevel
        actionResult["rc"] = 0
        return actionResult


class _philipshueLightOn(action._action):
    apiAddress = str()
    user = str()
    lightName = str()
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        lightName = helpers.evalString(self.lightName,{"data" : data})

        hueApi = hue.hue(apiAddress,user)
        lights = hueApi.getLights()
        result = hueApi.lightOn(lights[lightName])

        actionResult["result"] = result
        actionResult["rc"] = 0
        return actionResult

class _philipshueLightOff(action._action):
    apiAddress = str()
    user = str()
    lightName = str()
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        lightName = helpers.evalString(self.lightName,{"data" : data})

        hueApi = hue.hue(apiAddress,user)
        lights = hueApi.getLights()
        result = hueApi.lightOff(lights[lightName])

        actionResult["result"] = result
        actionResult["rc"] = 0
        return actionResult

class _philipshueGetLight(action._action):
    apiAddress = str()
    user = str()
    lightName = str()
    refreshLight = bool()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")

    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        lightName = helpers.evalString(self.lightName,{"data" : data})

        lights = cache.globalCache.get("philipshueList","lights",getPhilipshueList,apiAddress,user,dontCheck=self.refreshLight)
        if self.refreshLight:
            hueApi = hue.hue(apiAddress,user)
            lights[lightName] = hueApi.refreshLight(lights[lightName])

        actionResult["result"] = True
        actionResult["data"]["light"] = lights[lightName]
        actionResult["rc"] = 0
        return actionResult

class _philipshueGetLights(action._action):
    apiAddress = str()
    user = str()

    def __init__(self):
        cache.globalCache.newCache("philipshueList")
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})

        lights = cache.globalCache.get("philipshueList","lights",getPhilipshueList,apiAddress,user,forceUpdate=True)

        actionResult["result"] = True
        actionResult["data"]["lights"] = lights
        actionResult["rc"] = 0
        return actionResult

class _philipshueGroupOn(action._action):
    apiAddress = str()
    user = str()
    groupName = str()
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        groupName = helpers.evalString(self.groupName,{"data" : data})

        hueApi = hue.hue(apiAddress,user)
        groups = hueApi.getGroups()
        result = hueApi.groupOn(groups[groupName])

        actionResult["result"] = result
        actionResult["rc"] = 0
        return actionResult

class _philipshueGroupOff(action._action):
    apiAddress = str()
    user = str()
    groupName = str()
    
    def run(self,data,persistentData,actionResult):
        apiAddress = helpers.evalString(self.apiAddress,{"data" : data})
        user = helpers.evalString(self.user,{"data" : data})
        groupName = helpers.evalString(self.groupName,{"data" : data})

        hueApi = hue.hue(apiAddress,user)
        groups = hueApi.getGroups()
        result = hueApi.groupOff(groups[groupName])

        actionResult["result"] = result
        actionResult["rc"] = 0
        return actionResult

def getPhilipshueList(match,sessionData,apiAddress,user):
    if match == "sensors":
        hueApi = hue.hue(apiAddress,user)
        return hueApi.getSensors()
    elif match == "lights":
        hueApi = hue.hue(apiAddress,user)
        return hueApi.getLights()
    return None