import requests
from requests.auth import HTTPBasicAuth

TankUser = 'user@email'
TankPassword = 'password'


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


if __name__ == '__main__':
    get_tank_level()
