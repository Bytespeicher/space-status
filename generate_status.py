#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime

import requests
from jinja2 import Template

import config

api_data = json.loads(requests.get(config.API_URL).text)

for plugin in config.PLUGINS:
    try:
        plugin_module = getattr(
            __import__("plugins.%s" % plugin, plugin).__dict__[plugin], plugin
        )
    except Exception as e:
        print(e)
    api_data = plugin_module(api_data)


# The next part will generate the HTML for the status page
with open(config.SAVE_PATH, 'w') as f:
    f.write(json.dumps(api_data))
    f.close()

if api_data['state']['open'] is True:
    icon = api_data['icon']['open']
else:
    icon = api_data['icon']['closed']

html_template = Template(open(config.TEMPLATE_PATH).read())
html = html_template.render(
    status_open=api_data['state']['open'],
    status_lastchange=datetime.fromtimestamp(
        int(api_data['state']['lastchange'])).strftime('%H:%M:%S %d.%m.%Y'),
    status_message=api_data['state']['message'],
    status_icon=icon,
    logo=api_data['logo'],
    url=api_data['url'],
    location=api_data['location'],
    people_now_present=api_data['sensors']['people_now_present'][0]['value'],
    names=", ".join(api_data['sensors']['people_now_present'][0]['names']),
)

with open(config.HTML_PATH, 'wb+') as html_out:
    html_out.write(html)
