''' Fabric helper file '''


def set_env(config, env):
    ''' Set some default env values '''
    env.disable_known_hosts = True
    env.warn_only = True
    env.abort_on_prompts = True
    env.shell = "/bin/sh -c"
    if config['ssh']['gateway']:
        env.gateway = config['ssh']['gateway']
    env.user = config['ssh']['user']
    env.key = config['ssh']['key']
    return env
