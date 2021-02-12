# pycooks
collection of python help files

##json explorer
easily find value of key in json (dictonary in python)

###example code
here is an example code

```python
#openweathermap this kind of json data
data = {'coord': {'lon': 81.28, 'lat': 21.18}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 292.91, 'feels_like': 292.02, 'temp_min': 292.91, 'temp_max': 292.91, 'pressure': 1018, 'humidity': 67, 'sea_level': 1018, 'grnd_level': 984}, 'visibility': 10000, 'wind': {'speed': 2.81, 'deg': 53}, 'clouds': {'all': 100}, 'dt': 1606487301, 'sys': {'country': 'IN', 'sunrise': 1606438404, 'sunset': 1606477925}, 'timezone': 19800, 'id': 1272181, 'name': 'Delhi', 'cod': 200}
print(get(data,'temp'))
print(getaddr(data,'temp'))
```
