import requests

url = "http://127.0.0.1:11434/api/chat"
response = requests.get(url)
print("Status Code:", response.status_code)
print("Response Body:", response.text)
