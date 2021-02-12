import pyttsx3
import requests
import json
import time
class News():
    def __init__(self):
        self.__apikey='your api key'
        self.url='https://newsapi.org/v2/top-headlines?country=in&apiKey='+self.__apikey

    def get_top10_headlines(self):
        response = requests.get(self.url)
        news = json.loads(response.text)
        count=0
        for new in news['articles']:
            if count==10:
                break
            print(str(new['title']), "\n\n")
            print(str(new['description']), "\n\n")
            count+=1

try:
    n=News()
    n.get_top10_headlines()
except:
    print('WE HAVE ENCOUNTERED A PROBLEM MAKE SURE YOU ARE CONNECTED TO INTERNET')
