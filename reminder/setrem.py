#set reminder
import sqlite3
import re
import pyttsx3
import datetime
from word2number import w2n
from gtts import gTTS
import speech_recognition as spr

def speak(text):
    assistant.say(text)
    assistant.runAndWait()

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

        db = sqlite3.connect('data.db')
        c = db.cursor()
        c.execute('insert into ReminderData(title,datetime) values ( ? , ?)',(title,rdt))
        db.commit()
        speak('reminder set')
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
                tm = re.match('(\d+) hour.*',text).groups()
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
                tm = re.match('(\d+) minute.*',text).groups()
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
                recg.adjust_for_ambient_noise(source,duration=0.5)
                audio=recg.listen(source)
                query=recg.recognize_google(audio)
                query=query.lower()
                return query
        except:
            speak('sorry some error occured while listening , please try again')
            return None

if __name__ == '__main__':
    assistant = pyttsx3.init()
    rm = SetReminder()
    rm.gonoobs()
