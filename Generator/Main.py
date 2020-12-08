import sys
from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from Generator.ValidateConfig import ValidateConfig
from Generator.InstanceGenerator import InstanceGenerator


def run():
    try:
        configFile = "config/config.dat"
        print("AMMM Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        ValidateConfig.validate(config)
        print("Creating Instances...")
        instGen = InstanceGenerator(config)
        instGen.generate()
        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1


if __name__ == '__main__':
    sys.exit(run())
