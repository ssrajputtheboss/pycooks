from pycricbuzz import Cricbuzz
import pyttsx3
#c=Cricbuzz()
def speak(text):
    assistant.say(text)
    assistant.runAndWait()
class CricketScores():
    def __init__(self):
        self.c=Cricbuzz()
        self.all_matches = self.c.matches()
    def todays_matches(self):
        pass
    def all_matches_nearby(self):
        for match in self.all_matches:
            print(match['team1']['name'],'vs',match['team2']['name'])
    def all_matches_nearby_with_status(self):
        for match in self.all_matches:
            print(match['team1']['name'],'vs',match['team2']['name'])
            print(match['status'])
    def upcoming_matches(self):
        print('---ALL UPCOMING MATCHES---')
        count=0
        for match in self.all_matches:
            if 'Starts' in match['status']:
                count+=1
                print(match['team1']['name'],'vs',match['team2']['name'])
                print(match['status'])
        if count==0:
            print('No matches nearby')
    def live_scores(self):
        print('---LIVE SCORES---')
        count=0
        for match in reversed(self.all_matches):
            try:
                batting_data=self.c.livescore(match['id'])['batting']
                bowling_data=self.c.livescore(match['id'])['bowling']
                print(batting_data)
                print(batting_data['team'],':',batting_data['score'][0]['runs'],'/',batting_data['score'][0]['wickets'],'Overs:',batting_data['score'][0]['overs'])
                print('versus ',bowling_data['team'])
                print('status:',self.c.matchinfo(match['id'])['status'])
                count+=1
                #print(self.c.scorecard(match['id']))

                innings='second' if batting_data['score'][0]['inning_num']=='2' else 'first'
                assistant.say('match '+batting_data['team']+' versus '+bowling_data['team'])
                assistant.say(innings+' innings '+batting_data['team']+' is batting with score '+batting_data['score'][0]['runs']+' at '+batting_data['score'][0]['wickets'])
                speak('in '+batting_data['score'][0]['overs']+' overs')

            except:
                pass
        if count==0:
            print('NO LIVE MATCHES NOW')
                #print('This match is not live yet')
#print(c.matches())
assistant=pyttsx3.init()
try:
    cs=CricketScores()
    cs.upcoming_matches()
    cs.live_scores()
except:
    print('WE HAVE ENCOUNTERED A PROBLEM MAKE SURE YOU ARE CONNECTED TO INTERNET')
