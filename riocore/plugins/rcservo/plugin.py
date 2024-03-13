from riocore.plugins import PluginBase


class Plugin(PluginBase):
    def setup(self):
        self.NAME = "rcservo"
        self.TYPE = "joint"
        self.VERILOGS = ["rcservo.v"]
        self.PINDEFAULTS = {
            "pwm": {
                "direction": "output",
                "invert": False,
                "pullup": False,
            },
        }
        self.OPTIONS = {
            "frequency": {
                "default": 100,
                "type": int,
                "min": 20,
                "max": 150,
                "description": "update frequency",
            },
        }
        self.INTERFACE = {
            "position": {
                "size": 32,
                "direction": "output",
            },
            "enable": {
                "size": 1,
                "direction": "output",
                "on_error": False,
            },
        }
        self.SIGNALS = {
            "position": {
                "direction": "output",
                "min": -100,
                "max": 100,
                "scale": 10.0,
                "max_velocity": 1000.0,
                "description": "absolute position (-100 = 1ms / 100 = 2ms)",
            },
            "enable": {
                "direction": "output",
                "bool": True,
            },
        }
        self.INFO = "rc-servo output"
        self.DESCRIPTION = "to control rc-servos, usable as joint or as variable/analog output in LinuxCNC"

    def gateware_instances(self):
        instances = self.gateware_instances_base()
        instance = instances[self.instances_name]
        instance_predefines = instance["predefines"]
        instance_parameter = instance["parameter"]
        instance_arguments = instance["arguments"]
        freq = int(self.plugin_setup.get("frequency", self.OPTIONS["frequency"]["default"]))
        divider = self.system_setup["speed"] // freq
        instance_parameter["DIVIDER"] = divider
        return instances

    def convert(self, signal_name, signal_setup, value):
        if signal_name == "position":
            value = int((value + 300) * self.system_setup["speed"] / 200000)
        return value

    def convert_c(self, signal_name, signal_setup):
        if signal_name == "position":
            return """
            value = ((value + 300)) * OSC_CLOCK / 200000;
            """
        return ""
