'''
Runbook: Fact Finder

Identify facts about a specified host

  * Hostname

'''


import os
import json


system_info = {
  'hostname' : os.uname()[1],
  'os' : os.uname()[0],
  'kernel' : os.uname()[2],
}

print json.dumps(system_info)
