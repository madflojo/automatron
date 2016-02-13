'''

Runbook: Module for common tasks

'''

import argparse
import os
import sys
import yaml

def get_opts(description):
    ''' Parse command line arguments '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-c", "--config", dest="config", help="specify a configuration file")
    args = parser.parse_args()
    if args.config is None:
        parser.print_help()
    return args.config

def load_config(config):
    ''' Load config file into a dictionary '''
    if os.path.isfile(config):
        with open(config, "r") as fh:
            config = yaml.safe_load(fh)
            return config
    return None

def get_config(description=None):
    ''' Get configuration file from cmdline and get yaml from file '''
    config = get_opts(description)
    if config is None:
        sys.exit(1)
    else:
        config = load_config(config)
    if config is None:
        return False
    else:
        return config

if __name__ == '__main__':
    pass
