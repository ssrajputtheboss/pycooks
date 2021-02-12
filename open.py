import os
import re
import win32api
import sqlite3
import sys
class OpenSoftware():
    '''open any software'''
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
                    db=sqlite3.connect('data.db')
                    c=db.cursor()
                    c.execute('insert into savedpaths(fname,loc) values (\''+f+'\',\''+os.path.join(root, f)+'\');')
                    db.commit()
                    db.close()
                    os.system('\"'+os.path.join(root, f)+'\"')
                    #print(os.path.join(root, f))
                    return True# if you want to find only ones
    def gonoobs(self,sfname):
        try:
            os.startfile('\"'+sfname+'\"')
        except:
            try:
                db=sqlite3.connect('data.db')
                c=db.cursor()
                c.execute('select loc from savedpaths where fname like \''+sfname+'%.exe\'')
                path=c.fetchone()[0]
                os.system(path)
            except:
                if not self.find_file_in_all_drives(sfname):
                    print('file not found')

o=OpenSoftware()
i=input('enter:')
o.gonoobs(i)


#open google,youtube,software,file location
