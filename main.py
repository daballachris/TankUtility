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


def Main():
    jsonTokenResponse = requests.get('https://data.tankutility.com/api/getToken',
                                     auth=HTTPBasicAuth(TankUser, TankPassword)).json()
    jsonDeviceResponse = requests.get(
        'https://data.tankutility.com/api/devices?token=' + jsonTokenResponse[
            "token"]).json()
    # below is querying the first tank in the account - adjust the [0] if you want other tanks
    jsonTankDataResponse = requests.get(
        'https://data.tankutility.com/api/devices/' + jsonDeviceResponse["devices"][
            0] + '?token=' + jsonTokenResponse["token"]).json()

    print(jsonTankDataResponse["device"]["lastReading"]["tank"])

    putToOpenHAB('TankLevel', jsonTankDataResponse["device"]["lastReading"]["tank"])


if __name__ == '__main__':
    Main()
