import requests
import configparser


config_file = os.path.join(os.getenv('HOME'), '.djangollmapi')
config = configparser.ConfigParser(interpolation=None)
config.read(config_file)

API_KEY = config['PAPERSPACE']['API_KEY']
machine_id = config['PAPERSPACE']['MACHINE_ID']
headers = {'Authorization': f'Bearer {API_KEY}',
           'Content-Type': 'application/json'}


def check():
    url = 'https://api.paperspace.com/v1/machines'
    response = requests.get(url, headers=headers)
    state = response.json()['items'][0]['state']
    print(state)


def stop():
    url = f'https://api.paperspace.com/v1/machines/{machine_id}/stop'
    payload = {'id': machine_id}
    response = requests.patch(url, headers=headers, json=payload)
    print(response)
    print(response.content)


def start():
    url = f'https://api.paperspace.com/v1/machines/{machine_id}/start'
    payload = {'id': machine_id}
    response = requests.patch(url, headers=headers, json=payload)
    print(response)
    print(response.content)


# stop()
check()
