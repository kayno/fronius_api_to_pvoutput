# Fronius/pvoutput API tools

Add your inverter's IP, and pvoutput.org SID and API key to `config.py`.

Setting a static IP on your inverter is useful.

## AC voltage

Pushes AC voltage up to pvoutput

` /path/to/script/fronius_api_to_pvoutput/ac_voltage.py `

Run every 5 minutes via cron (4am to 10pm - should catch all the daylight):

`*/5 4-22 * * *  /path/to/script/fronius_api_to_pvoutput/ac_voltage.py`

Remember pvoutput API rate limiting (currently 60 req/hr): https://pvoutput.org/help/api_specification.html#rate-limits
