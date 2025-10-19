import requests

# Test the home endpoint
response = requests.get('http://127.0.0.1:5000/')
print('Home endpoint:')
print('Status:', response.status_code)
print('Response:', response.json())
print()

# Test the data endpoint
response = requests.get('http://127.0.0.1:5000/api/data')
print('Data endpoint:')
print('Status:', response.status_code)
print('Response:', response.json())
print()

# Test POST to data endpoint
data = {"name": "Test Item", "description": "Testing POST"}
response = requests.post('http://127.0.0.1:5000/api/data', json=data)
print('POST to data endpoint:')
print('Status:', response.status_code)
print('Response:', response.json())