import requests, json
from gtts import gTTS as g
import os
class WeatherReport():
    '''Uses openweathermap api to get current weather status
    of any city across the world'''
    def __init__(self):
        self.__base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        self.__api_key = 'your api key'
    def getcitytemprature(self,city):
        response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
        try:
           data= response.json()
           main = data['main']
           temperature = main['temp']
           temperature=round(temperature-273.15,2)
           print('the current temperature in '+CITY +' is '+str(temperature)+ ' degrees celcius')
        except:
            pass
    def getcitylatitude(self,city):
        response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
        data= response.json()
        return data['coord']['lat']
    def getcitylongitude(self,city):
        response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
        data= response.json()
        return data['coord']['lon']
    def normalweatherdata(self,city):
        response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
        data= response.json()
        print(data)
        print(type(data))
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        report = data['weather']
        temperature=round(temperature-273.15,2)
        print(f"{city:-^30}")
        print(f"Temperature: {temperature} degree celcius")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {report[0]['description']}")
        txt='the current temperature in '+city +' is '+str(temperature)+ ' degrees celcius'
        txt='the current temperature in '+city +' is '+str(temperature)+ ' degrees celcius'


#gtts stands for google text to speach
try:
    w=WeatherReport()
    c=input('city:')
    w.normalweatherdata(c)
except:
   print('WE HAVE ENCOUNTERED A PROBLEM MAKE SURE YOU ARE CONNECTED TO INTERNET')
