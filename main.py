import requests
from requests.auth import HTTPBasicAuth

# change these appropriately
openHABHostAndPort = 'http://192.168.1.216:8080'
TankUser = 'user@email'
TankPassword = 'password'


def putToOpenHAB(item, itemData):
    ItemURL = openHABHostAndPort + '/rest/items/' + item + '/state'
    OpenHABResponse = requests.put(ItemURL,
                                   data=str(itemData).encode('utf-8'),
                                   allow_redirects=True)


def get_tank_level():
    json_token_response = requests.get('https://data.tankutility.com/api/getToken',
                                       auth=HTTPBasicAuth(TankUser, TankPassword)).json()
    json_device_response = requests.get(
        'https://data.tankutility.com/api/devices?token=' + json_token_response[
            "token"]).json()
    # below is querying the first tank in the account - adjust the [0] if you want other tanks
    json_tank_data_response = requests.get(
        'https://data.tankutility.com/api/devices/' + json_device_response["devices"][
            0] + '?token=' + json_token_response["token"]).json()

    print(json_tank_data_response["device"]["lastReading"]["tank"])

    putToOpenHAB('TankLevel', json_tank_data_response["device"]["lastReading"]["tank"])


if __name__ == '__main__':
    get_tank_level()
