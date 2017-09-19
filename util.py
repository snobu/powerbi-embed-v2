import os
import sys
import yaml
import logging
import subprocess
from itertools import chain
log = logging.getLogger()

def setenv(conf_name="config.yml"):
    '''
    Settings configuration routine
    It reads the config.yml file and sets env vars (if not set)
    Settings can be set via the env variables with the same names
    in that case, env var takes priority
    '''
    try:
        with open(conf_name, "r") as f:
            settings = yaml.load(f)
    except FileNotFoundError:
        log.warning("Configuration config.yml not found; ignoring and going with env")
        return

    log.debug("loaded settings {}".format(settings) )
    for i in settings["env"]:
        if i not in os.environ:
            os.environ[i] = settings["env"][i]
            log.debug("set property {}".format(i))
        else:
            log.debug("{} env var already present".format(i))
    return settings['env']

def run_docker(img_name = "pbiembed"):
    ''' reading env vars and runs docker file '''
    env_vars = setenv()
    if env_vars is  None:
        with open("config.template.yml", "r") as f:
            env_vars = yaml.load(f)['env'].keys()
    #constructing a list of env vars
    var_string = tuple(chain(zip(["-e",]*len(env_vars),env_vars)))

    try:
        PORT = int(os.environ.get('PBI_SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    cmd = ["docker",  "run", "-p", "{}:{}".format(PORT,PORT)]
    cmd += var_string
    cmd.append(img_name)

    #log.debug("running command {}".format(" ".join(cmd)))
    log.debug("running command " + str(cmd))

    subprocess.Popen(cmd)

if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(stream = sys.stdout))
    if sys.argv[1] == "run_docker":
        run_docker()
    else:
        setenv()

