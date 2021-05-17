#!/usr/bin/python3

import config

import requests
import urllib
import json
from datetime import datetime
from argparse import ArgumentParser

# script args
parser = ArgumentParser()
parser.add_argument("-d", "--debug", dest="debug", default=False, help="Show what would be sent to pvoutput, but don't send it", action='store_true')
args = parser.parse_args()

debug = args.debug

inverter_url = "http://{}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData".format(config.inverter_ip)

try:
    inverter_data = requests.get(inverter_url, timeout=10)
except:
    if debug:
        print("Failed to connect to inverter API at {}".format(config.inverter_ip))
    exit()

if inverter_data.status_code == requests.codes.ok:
    inverter_data = inverter_data.json()
    ac_voltage = inverter_data['Body']['Data']['UAC']['Value'] if 'UAC' in inverter_data['Body']['Data'] else None
    energy_consumption = 0

    date_now = datetime.today().strftime('%Y%m%d')
    time_now = datetime.today().strftime('%H:%M')

    if debug:
        print("AC voltage: {}".format(ac_voltage))
        print("Energy consumption: {}".format(energy_consumption))
        print("date: {}".format(date_now))
        print("time: {}".format(time_now))
        print(json.dumps(inverter_data, indent=4, sort_keys=True))
    elif ac_voltage:
        pvoutput = requests.post(
            'https://pvoutput.org/service/r2/addstatus.jsp', 
            data={
                'd': str(date_now),
                't': str(time_now),
                'v3': str(energy_consumption),
                'v6': str(ac_voltage),
            },
            headers={
                'X-Pvoutput-Apikey': config.pvoutput_api_key,
                'X-Pvoutput-SystemId': config.pvoutput_sid,
            }, 
            timeout=10
        )

        if pvoutput.status_code != requests.codes.ok:
            print("Failed to send to pvoutput API: {} ({})".format(pvoutput.text, pvoutput.status_code))
else:
    print("Inverter API response not ok: {} ({})".format(inverter_data.text, inverter_data.status_code))
