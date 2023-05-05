import pyttsx3
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

chrome_options=Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless=True
Path="Database\\chromedriver.exe"
driver=webdriver.Chrome(Path,options=chrome_options)
driver.maximize_window()

website= r"https://ttsmp3.com/text-to-speech/British%20English/"
driver.get(website)
ButtonSelection=Select(driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[2]/form/select'))
ButtonSelection.select_by_visible_text('US English / Ivy')

def Speak(text):
    lenoftext=len(str(text))

    if lenoftext==0:
        pass

    else:
       
        print(f"AI : {text}.")
        data=  str(text)
        xpathofsec='/html/body/div[4]/div[2]/form/textarea'
        driver.find_element(By.XPATH,value=xpathofsec).send_keys(data)
        driver.find_element(By.XPATH,value='//*[@id="vorlesenbutton"]').click() 
        driver.find_element(By.XPATH,value='/html/body/div[4]/div[2]/form/textarea').clear()

        if lenoftext>=30:
            sleep(4)

        elif lenoftext>=40:
            sleep(6)    

        elif lenoftext>=70:
            sleep(10)    

        elif lenoftext>=55:
            sleep(8)    

        elif lenoftext>=100:
            sleep(13)    

        elif lenoftext>=120:
            sleep(14)

        else:
            sleep(2)


def Edit(text):
    """
    os.mkdir("d:\\newdir") # used to create new directory. 
    print(os.getcwd()) #returns the current working directory(CWD) of the file.
    os.chdir("d:\\")  #to change the current working directory.
    """
    engine=pyttsx3.init('sapi5')

    """voice"""
    voices=engine.getProperty('voices')  #changing voices
    #print(voices[0],voices[1],voices[2],voices[3],voices[4],voices[5],voices[6])
    engine.setProperty('voice',voices[6].id)

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 150)     # setting up new voice rate


    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    engine.say(text)
    print(text)
    engine.runAndWait()

Speak("hello sir")