#gets approximate location of user using ip address
# Python Program to Get IP Address
import socket
import requests
import json
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
url='http://api.ipstack.com/'+ip+'?access_key=5d24d973b3b4cbc17d9b0d8f51996241'
response = requests.get(url)
data = response.json()
print(data)
