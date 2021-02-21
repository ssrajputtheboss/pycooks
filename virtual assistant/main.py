import requests
import json
import pyttsx3
from geopy.distance import geodesic
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from pycricbuzz import Cricbuzz
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import time
import sqlite3
import re
import getpass
import datetime
import webbrowser
import wikipedia
import time
import win32api #install using pipwin
import wmi#new
from word2number import w2n#new
from plyer import notification#new
import os
import threading
import pyscreenshot as ss
from random import randint

#classes goes here-

class Screenshot():
    def gonoobs(self):
        img=ss.grab()
        img.save(main_path+self.getRandName())
        #file saved with 25 characters long random name
    def getRandName(self):
        name = ''
        for i in range(20):
            name+=chr(65+randint(0,25))
        for i in range(5):
            name+=str(randint(0,9))
        return name+'.png'

class PlaySong():
    def gonoobs(c):
        url='https://music.youtube.com/search?q='+c
        webbrowser.get('chrome').open_new_tab(url)

class WikiSearch():
    def gonoobs(query):
        results=wikipedia.summary(query, sentences=2)
        speak(results)


class SetReminder():
    def gonoobs(self):
        title = None
        while(title == None):
            speak('what do you want to be reminded')
            title=self.input_speech()
        rdt = None
        while(rdt== None):
            speak('when do you want it to be reminded')
            rdt=self.input_speech()
        print(rdt)
        rdt = self.extract_date_from_string(rdt)
        kill_process()#database rdata.db in use so need to kill the process
        db = sqlite3.connect(main_path+'\\rdata.db')
        c = db.cursor()
        c.execute('insert into ReminderData(title,datetime) values ( ? , ?)',(title,rdt))
        db.commit()
        speak('reminder set')
        #RESRTARTING PROCESS
        thread = threading.Thread(target = start_process,daemon=True)
        thread.start()
        time.sleep(4)#to restart process
        #c.close()
        #db.close()
    def extract_date_from_string(self,text):
        text = text.lower()
        text = self.modify_text(text)
        now = datetime.datetime.now()
        y,m,d,h,mn = now.year,now.month,now.day,now.hour,now.minute #default values
        #setting date
        if 'tommorow' in text:
            now += datetime.timedelta(days = 1)#getting tommorow's date
            y,m,d = now.year , now.month , now.day
        elif 'week' in text or 'weeks' in text:# after 1 week
            tm = re.match('(\d+) week.*').groups()
            if tm == None:#default case
                now += datetime.timedelta(days=7)
            else:
                now+=datetime.timedelta(days = 7*int(tm[0]))
            y,m,d = now.year , now.month , now.day
        else:
            #user has specified date on text or no date specified
            tm= self.getmonthday(text) #toget int month from string
            if tm!=None:
                d,m = tm
        #we got the date now time to get time
        if 'hour' in text or 'hours' in text:
            try:
                tm = re.match('.*(\d+) hour.*',text).groups()
                #print(tm)
                if tm == None:
                    tm=('1',)#default case
                if 'at' in text:
                    h=int(tm[0])
                else:
                    now += datetime.timedelta(hours = int(tm[0]))
                    y,m,d,h,mn = now.year,now.month,now.day,now.hour,now.minute
            except:
                pass
        if 'minute' in text or 'minutes' in text:
            try:
                tm = re.match('.*(\d+) minute.*',text).groups()
                #print(tm)
                if 'at' in text:
                    mn = int(tm[0])
                else:
                    now += datetime.timedelta(minutes = int(tm[0]))
                    y,m,d,h,mn = now.year,now.month,now.day,now.hour,now.minute
            except:
                pass

        if 'p.m.' in text or 'a.m.' in text or 'o\'clock' in text:
            tm = re.match('(\d+)\W(\d*) a\.m\..*|(\d+)\W(\d*) p\.m\..*|(\d+)\W(\d*) o\'clock.*',text).groups()
            if tm ==None:
                pass
            if len(tm)==1:
                h=int(tm[0])
                mn=0
            else :
                h,mn = int(tm[0]),int(tm[1])
            if 'a.m.' in text:
                if h>12:
                    h=h%12
            if 'p.m.' in text:
                if h<12:
                    h=12+h
        if 'morning' in text:
            h,mn = 8,0
        elif 'afternoon' in text:
            h,mn = 12,0
        elif 'evening' in text:
            h,mn = 18,0
        elif 'night' in text:
            h,mn = 23,59

        return datetime.datetime(y,m,d,h%24,mn%60)
    def modify_text(self,text):
        '''changes text numbers into digits'''
        words = re.split('\W+',text)
        for i in words:
            try:
                text.replace(i,str(w2n.word_to_num(i)))
            except:
                pass
        return text

    def getmonthday(self,text):
        day =datetime.datetime.now().day
        month=0
        mname=''
        if 'january' in text:
            mname = 'january'
            month = 1
        elif 'february' in text:
            mname = 'february'
            month = 2
        elif 'march' in text:
            mname = 'march'
            month = 3
        elif 'april' in text:
            mname = 'april'
            month = 4
        elif 'may' in text:
            mname = 'may'
            month = 5
        elif 'june' in text:
            mname = 'june'
            month = 6
        elif 'july' in text:
            mname = 'july'
            month = 7
        elif 'august' in text:
            mname = 'august'
            month = 8
        elif 'september' in text:
            mname = 'september'
            month = 9
        elif 'october' in text:
            mname = 'october'
            month = 10
        elif 'november' in text:
            mname = 'november'
            month = 11
        elif 'december' in text:
            mname = 'december'
            month = 12
        if month!=0:
            tm = re.match('(\d+).*'+mname).groups()
            if tm == None:
                return day,month
            else:
                return int(tm[0]),month
        return None

    def input_speech(self):
        try:
            recg=spr.Recognizer()
            with spr.Microphone() as source:
                recg.adjust_for_ambient_noise(source,duration=0.2)
                audio=recg.listen(source)
                query=recg.recognize_google(audio)
                query=query.lower()
                return query
        except:
            speak('sorry some error occured while listening , please try again')
            return None

class OpenSoftware():
    '''opens any software'''
    def find_file_in_all_drives(self,file_name):
        #create a regular expression for the file
        rex = re.compile(file_name+'[a-zA-Z0-9 ]*'+'\.exe')
        for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
            b=self.find_file( drive, rex )
            if b:
                return True
    def find_file(self,root_folder, rex):
        for root,dirs,files in os.walk(root_folder):
            for f in files:
                result = rex.search(f)
                if result:
                    print(str(f))
                    print(root+'\\'+str(f))
                    os.system('\"'+os.path.join(root, f)+'\"')
                    #print(os.path.join(root, f))
                    return True# if you want to find only ones
    def gonoobs(self,sfname):
        if 'command' in sfname or 'prompt' in sfname:
            sfname = 'cmd'
        try:
            os.startfile('\"'+sfname+'\"')
        except:
            if not self.find_file_in_all_drives(sfname):
                print('file not found')


class LiveScores():
    def __init__(self):
        self.c=Cricbuzz()
        self.all_matches = self.c.matches()
    def gonoobs(self):
        print('---LIVE SCORES---')
        count=0
        for match in reversed(self.all_matches):
            try:
                batting_data=self.c.livescore(match['id'])['batting']
                bowling_data=self.c.livescore(match['id'])['bowling']
                '''
                print(batting_data)
                print(batting_data['team'],':',batting_data['score'][0]['runs'],'/',batting_data['score'][0]['wickets'],'Overs:',batting_data['score'][0]['overs'])
                print('versus ',bowling_data['team'])
                print('status:',self.c.matchinfo(match['id'])['status'])
                count+=1
                #print(self.c.scorecard(match['id']))
                '''
                count+=1
                innings='second' if batting_data['score'][0]['inning_num']=='2' else 'first'
                assistant.say('match '+batting_data['team']+' versus '+bowling_data['team'])
                assistant.say(innings+' innings '+batting_data['team']+' is batting with score '+batting_data['score'][0]['runs']+' at '+batting_data['score'][0]['wickets'])
                speak('in '+batting_data['score'][0]['overs']+' overs')

            except:
                pass
        if count==0:
            speak('NO LIVE MATCHES NOW')


class Temperature():
    def __init__(self):
        self.__base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        self.__api_key = '1d0e999398d111f7c2c2b0a0852fb4d8'

    def gonoobs(self,city):
        try:
            response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
            temperature = response.json()['main']['temp']
            temperature=round(temperature-273.15,2)
            text='the current temperature in '+city +' is '+str(temperature)+ ' degrees celcius'
            speak(text)
        except:
            speak('Sorry can not find temprature now , make sure you are connected to the internet')

class WeatherReport():
    '''Uses openweathermap api to get current weather status
    of any city across the world'''
    def __init__(self):
        self.__base_url = "http://api.openweathermap.org/data/2.5/weather?q="
        self.__api_key = '1d0e999398d111f7c2c2b0a0852fb4d8'
    def gonoobs(self,city):
        try:
            response = requests.get(self.__base_url+city+"&appid="+self.__api_key)
            data= response.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            report = data['weather']
            temperature=round(temperature-273.15,2)
            txt1='the current temperature in '+city +' is '+str(temperature)+ ' degrees celcius'
            txt2='and the current weather is ' + str(report[0]['description'])
            speak(txt1+txt2)
        except:
            speak('Sorry can not find weather details now ')
class UpcomingMatches():
    def __init__(self):
        self.c=Cricbuzz()
        try:
            self.all_matches = self.c.matches()
        except :
            self.all_matches=None
    def gonoobs(self):
        if self.all_matches == None:
            speak('Cannot find match details now')
            return
        matches_available=False
        for match in self.all_matches:
            if 'Starts' in match['status']:
                matches_available = True
                assistant.say('match '+match['team1']['name']+'vs'+match['team2']['name'])
                assistant.say(match['status'])
                assistant.runAndWait()
        if not matches_available:
            speak('No matches in nearby future')

class DistanceFinder():
    def __init__(self):
        self.geolocator = Nominatim(user_agent="p_finder")
    def gonoobs(self,loc1,loc2):
        try:
            l1 = self.geolocator.geocode(loc1)
            l2 = self.geolocator.geocode(loc2)
            start_point=(float(l1.longitude),float(l1.latitude))
            end_point=(float(l2.longitude),float(l2.latitude))
            d=round(geodesic(start_point,end_point).kilometers,2)
            #d2=round(great_circle(start_point,end_point).kilometers,2)
            speak('approximate distance between '+loc1+' and '+loc2+' is '+str(d)+' kilometers')
        except:
            speak('cannot find distance make sure you are connected to the internet')
class News():
    def __init__(self):
        self.__apikey='e91abf1c8a1147b4813b9dbbd87fb0bc'
        self.url='https://newsapi.org/v2/top-headlines?country=in&apiKey='+self.__apikey
        self.total_count=5

    def gonoobs(self):
        try:
            response = requests.get(self.url)
            newscollection = json.loads(response.text)
            count=0
            speak('Top 5 news headlines are as follows')
            for news in newscollection['articles']:
                if count==self.total_count:
                    break
                assistant.say(str(news['title']))
                count+=1
            assistant.runAndWait()
        except:
            speak('sorry cannot load news at this time')


#new classes above this line, all functions below this line
def speak(text):
    assistant.say(text)
    assistant.runAndWait()

def wish(master):
    hour=int(datetime.datetime.now().hour)

    if hour>4 and hour <12:
        #print('Good Morning!'+master)
        speak('Good Morning!'+master)
    elif hour>=12 and hour<18:
        #print('Good Afternoon!'+master)
        speak('Good Afternoon!'+master)
    else:
        #print('Good Evening!'+master)
        speak('Good Evening!'+master)
    #print('How may I help you?')
    speak('How may I help you?')

def isProcessRunning():
    f = wmi.WMI()
    for process in f.Win32_Process():
    	if 'pythonw' in process.Name.lower():
            return True
    return False

def start_process():
    if not isProcessRunning():
        os.system('pythonw \"'+main_path+'\"')

def kill_process():
	os.system('taskkill /F /IM pythonw.exe /T')

def run_assistant():

    c = db.cursor()
    #input
    #speak('i am listening')
    #query=input('command: ')#command,Object,attributecount
    query=''#default
    try:
        recg=spr.Recognizer()
        with spr.Microphone() as source:
            recg.adjust_for_ambient_noise(source,duration=0.2)
            audio=recg.listen(source)
            query=recg.recognize_google(audio)
            query=query.lower()
        print('\''+query+'\'')
    except:
        speak('sorry some error occured while listening , please try again')
        return

    c.execute('select * from commandtofunction where \''+query+'\' like command;')
    try:
        cmd,o,cnt=c.fetchone()
    except:
        speak('cannot find command')
        return
    o=eval(o)
    cmd=cmd.replace('%','(.*)')
    try:
        attributes=list(re.match(cmd,query).groups())
    except:
        speak('sorry cannot find command')
        return
    #print(cnt,len(attributes))
    if cnt==0:
        o.gonoobs()
        return
    if cnt==len(attributes):
        exec='o.gonoobs(\''+attributes[0]+'\''
        for i in range(1,len(attributes)):
            exec=exec+',\''+attributes[i]+'\''
        exec+=')'
        eval(exec)
    else:
        speak('sorry cannot find command')

if __name__ == '__main__':
    assistant=pyttsx3.init()
    main_path = __file__.replace('main.py' , '')
    chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
    endprocess = False
    #start_process()
    #if start_process() is directly called then program has to wait until it finishes
    #execution which will take infinite time so using thread problem is solved
    thread = threading.Thread(target = start_process,daemon=True)
    thread.start()
    db = sqlite3.connect('data.db')
    wish(getpass.getuser())
    run_assistant()
    '''
    try:
        db = sqlite3.connect('data.db')
        wish(getpass.getuser())
        run_assistant()
    except:
        speak('an error occured')
    '''
