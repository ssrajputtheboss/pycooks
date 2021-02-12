import pyscreenshot as ss
from random import randint
class Screenshot():
    def gonoobs(self):
        img=ss.grab()
        img.save('C:\\Users\\shash\\Desktop\\python project\\'+self.getRandName())
        #file saved with 25 characters long random name
    def getRandName(self):
        name = ''
        for i in range(20):
            name+=chr(65+randint(0,25))
        for i in range(5):
            name+=str(randint(0,9))
        return name+'.png'
Screenshot().gonoobs()
