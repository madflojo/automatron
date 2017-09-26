''' Fabric helper file '''


def set_env(config, env, override="default"):
    ''' Set some default env values '''
    env.disable_known_hosts = True
    env.warn_only = True
    env.abort_on_prompts = False
    env.shell = "/bin/sh -c"
    if "ssh" in config:
        if config['ssh']['gateway']:
            env.gateway = config['ssh']['gateway']
        env.user = config['ssh']['user']
        env.key = config['ssh']['key']
    else:
        if config['credentials'][override]['gateway']:
            env.gateway = config['credentials'][override]['gateway']
        env.user = config['credentials'][override]['user']
        env.key = config['credentials'][override]['key']
    return env
