# pycooks
collection of python help files. some of these are useful for creating a virtual assistant using python.

## json explorer
easily find value of key in json (dictonary in python)

### example code
here is an example code

```python 
import jsonexplorer as je
#openweathermap api sends this kind of json data
data = {'coord': {'lon': 81.28, 'lat': 21.18}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 292.91, 'feels_like': 292.02, 'temp_min': 292.91, 'temp_max': 292.91, 'pressure': 1018, 'humidity': 67, 'sea_level': 1018, 'grnd_level': 984}, 'visibility': 10000, 'wind': {'speed': 2.81, 'deg': 53}, 'clouds': {'all': 100}, 'dt': 1606487301, 'sys': {'country': 'IN', 'sunrise': 1606438404, 'sunset': 1606477925}, 'timezone': 19800, 'id': 1272181, 'name': 'Delhi', 'cod': 200}
print(je.get(data,'temp'))
print(je.getaddr(data,'temp'))
```

# news.py

uses newsapi to get latest news headlines. API key is required.

# open.py

python program to open any software in windows computer(uses win32api so it works only on windows) .
If a program is not found it searches in all drives and at all file locations.

# noti.py

program to create a notification on desktop , uses plyer module.

# process_check.py

program to check if a process is currently running in the background(windows) and how to kill a process progamatacally. uses wmi and subprocess modules.

# quote.py

printing a random quote using quotes module.

# score.py

get latest cricket scores using pycricbuzz library.

# ss.py

taking a screenshot using python code. uses pyscreenshot library. there are also alternatives available for the same work but pyscreenshot does it in the minimum code.

# weather.py

getting weather data of a city using openweathermap api. api key is required.
