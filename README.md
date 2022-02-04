# TankUtility
Propane tank level displayed on a oled screen. Queries the [Tank Utility API](http://apidocs.tankutility.com/) from an ESP8266 device, and displays the result.
## Configuration
Create a configuration.json file:
```
{
"Security": 
	{
	"User": "",
	"Password": ""
	},
"WiFi": 
	{
	"SSID": "",
	"Password": ""
	}
}
```

## Credits
Took inspiration from [this](https://community.openhab.org/t/propane-tank-monitor-tankutility-python-script/91331) post.
