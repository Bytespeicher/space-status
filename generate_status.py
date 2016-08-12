#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from datetime import datetime

import requests
from jinja2 import Template

import config

api_data = config.API_DATA.copy()

try:
    new_api_data = json.loads(requests.get(config.API_URL, timeout=5).text)
    api_data.update(new_api_data)
except (requests.ReadTimeout, requests.ConnectionError):
    print("Error while connecting to status GW, using defaults")

for plugin in config.PLUGINS:
    try:
        plugin_module = getattr(
            __import__("plugins.%s" % plugin, plugin).__dict__[plugin], plugin
        )
    except Exception as e:
        print(e)

    old_data = api_data
    try:
        api_data = plugin_module(api_data)
    except:
        api_data = old_data


# The next part will generate the HTML for the status page
with open(config.SAVE_PATH, 'w') as f:
    f.write(json.dumps(api_data))
    f.close()

if api_data['state']['open'] is True:
    icon = api_data['icon']['open']
else:
    icon = api_data['icon']['closed']

if 'names' in api_data['sensors']['people_now_present'][0]:
    people = ", ".join(api_data['sensors']['people_now_present'][0]['names'])
else:
    people = ""

html_parser_args = {
    'status_open': api_data['state']['open'],
    'status_lastchange': datetime.fromtimestamp(
        int(api_data['state']['lastchange'])).strftime('%H:%M:%S %d.%m.%Y'),
    'status_message': api_data['state']['message'],
    'status_icon': icon,
    'logo': api_data['logo'],
    'url': api_data['url'],
    'location': api_data['location'],
    'people_now_present': api_data['sensors']['people_now_present'][0]['value'],
    'names': people,
    'temperatures': False,
}

for plugin in config.PLUGINS:
    try:
        plugin_module = getattr(
            __import__("plugins.%s" % plugin, plugin).__dict__[plugin],
            plugin + "_html"
        )
    except Exception as e:
        print(e)

    old_args = html_parser_args
    try:
        html_parser_args = plugin_module(api_data, html_parser_args)
    except:
        html_parser_args = old_args

html_template = Template(open(config.TEMPLATE_PATH).read().decode('utf-8'))
html = html_template.render(**html_parser_args)

with open(config.HTML_PATH, 'wb+') as html_out:
    html_out.write(html.encode('utf-8'))
