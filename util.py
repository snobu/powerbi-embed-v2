import os
import sys
import yaml
import logging
log = logging.getLogger()
'''
Settings configuration routine
It reads the config.yml file and sets env vars (if not set)
Settings can be set via the env variables with the same names
in that case, env var takes priority
'''
def setenv(conf_name="config.yml"):
    with open(conf_name, "r") as f:
        settings = yaml.load(f)
    log.debug("loaded settings {}".format(settings) )
    for i in settings["env"]:
        if i not in os.environ:
            os.environ[i] = settings["env"][i]
            log.debug("set property {}".format(i))
        else:
            log.debug("{} env var already present".format(i))

if __name__ == '__main__':
    log.setLevel(logging.WARNING)
    log.addHandler(logging.StreamHandler(stream = sys.stdout))
    setenv()

