Status tools
============

These tools are used to display status information of our hackerspace.

There's a simple Python script that generates a HTML page from a jinja2 template
and a script aggregating the status JSON from a WiFi router.

`connected_devices`, `connected_users` and `generate_spaceapi` run on a WiFi router and collect 
information about the devices in our WiFi network to tell wether someone is 
connected and thus the space is open. This is of course just an approximation 
but it's cheap and works pretty well with a low DHCP lease time.

### Usage: ###

* Copy `config.py.example` to `config.py` and adapt settings (at least file paths for output and includes)
* Copy `includes/` folder to the build folder specified in `config.py`

* execute `python generate_status.py`