import requests
import json

url = 'http://localhost:8000/generate?text=こんにちは'
response = requests.get(url)
json_data = response.json()

print(json_data)
print(json_data['message'])
