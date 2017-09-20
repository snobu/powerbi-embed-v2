import os
import sys
import yaml
import logging
import subprocess
from itertools import chain
log = logging.getLogger()

def get_settings(conf_name="config.yml", set_env = True):
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
    if set_env:
        for i in settings["env"]:
            if i not in os.environ:
                os.environ[i] = settings["env"][i]
                log.debug("set property {}".format(i))
            else:
                log.debug("{} env var already present".format(i))
    return settings

def run_docker(img_name = "pbiembed"):
    ''' reading env vars and runs docker file '''
    env_vars = get_settings()
    if env_vars is  None:
        with open("config.template.yml", "r") as f:
            env_vars = yaml.load(f)['env'].keys()
    else:
        env_vars = env_vars['env']
    #constructing a list of env vars to pass to command line
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

def read_settings_app():
    #read settings
    settings = get_settings(set_env=False)
    if 'app' not in settings:
        log.error("Application settings are not present in the config file. Add app section, see the doc")
        raise ValueError("Missing settings for application")
    return settings

def get_create_plan_cmd(settings):
    cmd = ("az appservice plan create --sku {sku} --is-linux -l " +
                "{region} -n {plan_name} -g {resource_group}").format(**settings['app'])

    log.debug("create plan cmd :\n" + cmd )
    return cmd

def get_webapp_cmd(settings):
    cmd = ("az webapp create -n {app_name} -g {resource_group} " +
                "--plan {plan_name} -i {container_name}").format(**settings['app'])

    log.debug("create app cmd :\n" + cmd )
    return cmd

def get_settings_cmd(settings):
    cmd = ("az webapp config appsettings set -g {resource_group} " +
                "-n {app_name} --settings ").format(**settings['app'])
    env_vars = ['{}="{}"'.format(a,b) for a, b in settings['env'].items()]
    cmd += " ".join(env_vars)

    log.debug("Set app settings cmd :\n" + cmd )
    return cmd

def get_restart_cmd(settings):
    cmd = ("az webapp restart -g {resource_group} -n {app_name}").format(**settings['app'])

    log.debug("Restart app cmd :\n" + cmd )
    return cmd

def delete_webapp():
    settings = read_settings_app()

    cmd =  "az webapp delete -n {app_name} -g {resource_group}".format(**settings['app'])
    log.debug("delete app command: \n" + cmd)
    subprocess.call(cmd,shell=True)

def create_webapp(dry_run = False):
    '''
    A helper routine that either runs or prints az commands to install your web app.
    Settings for web app must be configured in config.yml "app" section.
    You need to first run az login and az account set to use it
    '''

    settings = read_settings_app()

    commands = []
    commands.append(get_create_plan_cmd(settings))
    commands.append(get_webapp_cmd(settings))
    commands.append(get_settings_cmd(settings))
    commands.append(get_restart_cmd(settings))

    for cmd in commands:
        if dry_run:
            print(cmd)
        else:
            subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(stream = sys.stdout))
    if sys.argv[1] == "run_docker":
        run_docker()
    elif sys.argv[1] == "create_app":
        dry = len(sys.argv)>2 and (sys.argv[2] in ("-d" , "--dry"))
        create_webapp(dry_run=dry)
    elif sys.argv[1] == "delete_app":
        delete_webapp()
    elif sys.argv[1] == "setenv":
        get_settings(set_env = True)
    else:
        print("Usage: python util.py [run_docker|create_app|delete_app|setenv] [-d|--dry]")

