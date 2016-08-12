# -*- coding: iso-8859-15 -*-

import requests
import json

import config


def temperature(data):
    temperature = []
    try:
        for url in config.PLUGINS['temperature']['urls']:
            temp_json = json.loads(requests.get(url, timeout=5).text)
            for loc, temp in temp_json.items():
                temperature_item = {
                    'value': temp,
                    'unit': '°C',
                    'location': loc
                }
                temperature.append(temperature_item)
    except Exception as e:
        print("TEMPERATURE: Unexpected error")
        print(e)

    data['sensors']['temperature'] = temperature

    return data


def temperature_html(data, args):
    if 'sensors' in data and 'temperature' in data['sensors']:
        args['temperatures'] = data['sensors']['temperature']

    return args
