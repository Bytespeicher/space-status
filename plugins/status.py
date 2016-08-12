# -*- coding: utf-8 -*-

import json
import requests

import config


def status(api_data):
    try:
        new_api_data = json.loads(
            requests.get(config.PLUGINS['status']['url'], timeout=5).text)
        api_data.update(new_api_data)
    except (requests.ReadTimeout, requests.ConnectionError):
        print("Error while connecting to status GW, using defaults")
    return api_data
