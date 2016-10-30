Status tools
============

These tools are used to display status information of our hackerspace.

There's a simple Python script that generates a HTML page from a jinja2 template
and a script aggregating the status JSON from a WiFi router.

`connected_devices`, `connected_users` and `generate_spaceapi` run on a WiFi router and collect 
information about the devices in our WiFi network to tell wether someone is 
connected and thus the space is open. This is of course just an approximation 
but it's cheap and works pretty well with a low DHCP lease time.

### File description ###

* **connected_devices** - script called by plugin to get number of devices
* **connected_users** - script called by plugin to get names of users by mac address
* **config.py.example** - configuration for paths and default api content; to be renamed to config.py
* **generate_spaceapi** - file to be called by user to collect data (by plugins) and write spaceapi.json file
* **spaceapi.json** - generated file, holds information for client applications and web-services
* **generate_status.py** - script to be called by user that reads spaceapi.json and creates html info page

to be cntinued ...


### Usage: ###

* Copy `config.py.example` to `config.py` and adapt settings (at least file paths for output and includes)
* Copy `includes/` folder to the build folder specified in `config.py`
* Copy `images/` folder to the build folder specified in `config.py` and `status_template`


* execute `ash generate_spaceapi`
* execute `python generate_status.py`

### States: ###

Api(0.13) compatible states:
* **None** - undefined
* **true** - open
* **false** - closed

non-api compatible states
* **"members_only"** - open, but members only

Additional states can be defined in generate_spaceapi and used in generate_status.py and status_template
