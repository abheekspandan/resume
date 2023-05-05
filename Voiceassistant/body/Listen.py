import pyttsx3
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import speech_recognition as sr
from googletrans import Translator
import openai
from dotenv import load_dotenv

def takecommand():                      
    command=sr.Recognizer()

    with sr.Microphone() as source:
        command.adjust_for_ambient_noise(source)
        print("listening...")  
        command.pause_threshold=1
        audio=command.listen(source,0,8)    

    try:
        #using default API u can change it chk documentation
        print("Recognizing...")
        query=command.recognize_google(audio,language='en',show_all=False)
        #print("user said:", query ) for hindi printing  

    except sr.RequestError as e:
        speak("Say that again please...".format(e))
        return ""

    query=str(query).lower()    
    return query


def TranslationHintoEng(Text):    
    line=str(Text)
    translate=Translator()
    result=translate.translate(line,dest='en') 
    data=result.text
    print(f"You : {data}.") 
    return data

def MicExecution():
    query=takecommand()
    data=query
   # data=TranslationHintoEng(query)
    return data


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

def speak(text):
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


def speak2(text):
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


# open AI
fileopen=open("data\\api.txt","r")
API=fileopen.read()
fileopen.close()
print(API)


openai.api_key=API
load_dotenv()
completion=openai.Completion()

def ReplyBrain(questions,chat_log=None):
    FileLog=open("Database\\chat_log.txt","r")
    chat_log_template=FileLog.read()
    FileLog.close()

    if chat_log is None:
        chat_log=chat_log_template

    prompt=f'{chat_log}You : {questions}.\nAlice : '
    response=completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0)    
    answer=response.choices[0].text.strip()
    chat_log_template_update=chat_log_template+f"\nYou : {questions}. \nAlice : {answer}."
    FileLog=open("Database\\chat_log.txt","w")
    FileLog.write(chat_log_template_update)
    FileLog.close()
    return answer 

#TranslationHintoEng("और भाई क्या हाल है")      
query=MicExecution()
if 'alice' in query:
    speak2("hello sir")
    while True:
        reply=ReplyBrain(MicExecution())  
        speak2(reply)