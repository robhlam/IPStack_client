#!/usr/bin/env python3
'''
Python script to query IPStack API for the latitude and
longitude of a given IP address.

Returns json.

Security isn't excellent (the free API is http!) but this
makes it easier for the user to do the right thing and
store the API key in a file with restrictive permissions.

With this script the API key doesn't appear in the process
environment or arguments (which can be visible to other
users on the machine).

The key may appear in stderr if an exception is raised.
'''

import ipaddress
import json
import os
import requests
import sys

from pathlib import Path

API_KEY_PATH = Path('~/.robert_lamont_brightsign_ipstack_key').expanduser()


def opener(path, flags):
  "Opens a file with only user read and write permissions."
  return os.open(path, flags, 0o600)


def get_api_key_from_disk_or_user(path=API_KEY_PATH):
  try:
    with open(path) as f:
      return f.read().strip()
  except FileNotFoundError:
    if sys.stdout.isatty(): # interactive
      api_key = input('No API key found. Please enter the key to save it:\n')
      with open(path, 'w', opener=opener) as f:
        f.write(api_key)
      print('Saved.\n')
      return api_key
    else: # not interactive
      print("No API key found. Please run interactively to save one.", file=sys.stderr)


if __name__ == '__main__':
  try:
    ip = ipaddress.ip_address(sys.argv[1])
    api_key = get_api_key_from_disk_or_user()
    url = f'http://api.ipstack.com/{ip}?access_key={api_key}'
    response = json.loads(requests.get(url).content)
    if response.get('success', True) is False:
      print("Response from server:\n",
            json.dumps(response, indent=2),
            file=sys.stderr)
      exit(-1)
    else:
      print(json.dumps({"longitude": response['longitude'], "latitude": response['latitude']}, indent=2))
  except:
    this_script = Path(sys.argv[0]).name
    print(f'''Usage:
{this_script} ip.add.re.ss

The API key is stored at
{API_KEY_PATH}
''', file=sys.stderr)
    raise
