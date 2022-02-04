import binascii
import json
import network

CHUNK_SIZE = 64
config_data = json.load(open('configuration.json'))


def http_get(url, user=None, password=None):
    import socket
    _, _, host, path = url.split('/', 3)
    address = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(address)

    headers = 'GET /%s HTTP/1.1\r\nHost: %s\r\n' % (path, host)

    if user is not None and password is not None:
        authentication_string = user + ":" + password
        authentication_string = authentication_string.encode('ascii')
        headers += "Authorization: Basic " + binascii.b2a_base64(authentication_string).strip().decode('ascii')
        headers += '\r\n'

    headers += '\r\n'

    s.send(bytes(headers, 'utf8'))

    response = ""
    try:
        data = s.recv(CHUNK_SIZE)
        response += data.decode()
        while len(data) > 0:
            data = s.recv(CHUNK_SIZE)
            response += data.decode()
    except:  # Exception is different on device (socket.timeout in Python), just catching them all.
        pass

    s.close()

    response = response.split('\x0D\x0A\x0D\x0A', 1)[1]

    return response


def get_tank_level():
    json_token_response = json.loads(http_get('https://data.tankutility.com/api/getToken',
                                              user=config_data['Security']['User'],
                                              password=config_data['Security']['Password']))
    json_device_response = json.loads(http_get('https://data.tankutility.com/api/devices?token='
                                               + json_token_response["token"]))
    json_tank_data_response = json.loads(http_get('https://data.tankutility.com/api/devices/'
                                                  + json_device_response["devices"][0]
                                                  + '?token=' + json_token_response["token"]))

    print("*" * 25)
    print("Tank Level:", json_tank_data_response["device"]["lastReading"]["tank"])
    print("Temperature:", json_tank_data_response["device"]["lastReading"]["temperature"])


if __name__ == '__main__':
    try:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(config_data['WiFi']['SSID'], config_data['WiFi']['Password'])
        sta_if = network.WLAN(network.STA_IF)

        while not sta_if.isconnected():
            print("Waiting for wifi...")
    except AttributeError:
        print("Not running on ESP8266 device, skipping network check.")

    get_tank_level()
