from core import plugin, model

class _philipshue(plugin._plugin):
    version = 0.33

    def install(self):
        # Register models
        model.registerModel("philipshueMotionDetected","_philipshueMotionDetected","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueLightOn","_philipshueLightOn","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueLightOff","_philipshueLightOff","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGroupOn","_philipshueGroupOn","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGroupOff","_philipshueGroupOff","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGetSensor","_philipshueGetSensor","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueLighThreshold","_philipshueLighThreshold","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGetLight","_philipshueGetLight","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGetLights","_philipshueGetLights","_action","plugins.philipshue.models.action")
        model.registerModel("philipshueGetSensors","_philipshueGetSensors","_action","plugins.philipshue.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("philipshueMotionDetected","_philipshueMotionDetected","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueLightOn","_philipshueLightOn","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueLightOff","_philipshueLightOff","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGroupOn","_philipshueGroupOn","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGroupOff","_philipshueGroupOff","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGetSensor","_philipshueGetSensor","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueLighThreshold","_philipshueLighThreshold","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGetLight","_philipshueGetLight","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGetLights","_philipshueGetLights","_action","plugins.philipshue.models.action")
        model.deregisterModel("philipshueGetSensors","_philipshueGetSensors","_action","plugins.philipshue.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        if self.version < 0.33:
            model.registerModel("philipshueGetLights","_philipshueGetLights","_action","plugins.philipshue.models.action")
            model.registerModel("philipshueGetSensors","_philipshueGetSensors","_action","plugins.philipshue.models.action")
        if self.version < 0.32:
            model.registerModel("philipshueGetLight","_philipshueGetLight","_action","plugins.philipshue.models.action")
        if self.version < 0.31:
            model.registerModel("philipshueLighThreshold","_philipshueLighThreshold","_action","plugins.philipshue.models.action")
        if self.version < 0.3:
            model.registerModel("philipshueGetSensor","_philipshueGetSensor","_action","plugins.philipshue.models.action")
        if self.version < 0.2:
            model.registerModel("philipshueGroupOn","_philipshueGroupOn","_action","plugins.philipshue.models.action")
            model.registerModel("philipshueGroupOff","_philipshueGroupOff","_action","plugins.philipshue.models.action")
