import requests
import yaml

# Config
with open('../../../config/server_address.yaml', 'r') as yml:
    api_config = yaml.safe_load(yml)
locaddr = (api_config['host'], api_config['port'])

text = 'こんにちは'
url = 'http://' + str(api_config['host']) + ':' + \
    str(api_config['port']) + '/generate?text=' + text
response = requests.get(url)
json_data = response.json()

print(json_data)
print(json_data['message'])
