import requests
import configparser
from requests.auth import HTTPBasicAuth

# Read user configuration data from configuration.ini
config = configparser.ConfigParser()
file_name = 'configuration.ini'
config.read(file_name)

TankUser = config['SECURITY']['TankUser']
TankPassword = config['SECURITY']['TankPassword']


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
