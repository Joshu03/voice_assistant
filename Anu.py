#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/RajiRai/Voice-Assistant/blob/main/Minchu.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[ ]:




# In[ ]:

import sqlite3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import time
import requests
import subprocess #process various system commands like to log off or to restart your system
#from ecapture import ecapture as ec #for capturing photos 
import playsound # to play saved mp3 file 
from gtts import gTTS # google text to speech 
import os # to save/open files 
import wolframalpha # to calculate strings into formula 
from selenium import webdriver # to control browser operations 


# In[ ]:
#def dataupload:
#    conn = sqlite3.connect('search.db')
 #   c = conn.cursor()

    #c.execute('''CREATE TABLE asch(sch TEXT,id INT PRIMARY KEY)''')


  #  schc = 'who are you'
   # wht = 'what can you do'
    #c.execute('''INSERT INTO asch VALUES(?,?)''',(schc,wht,))

    #conn.commit()


conn = sqlite3.connect('search_data.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS experiments')
cur.execute('CREATE TABLE experiments (sch TEXT, id INTEGER PRIMARY KEY)')
conn.commit()






def talk():
    input=sr.Recognizer()
    with sr.Microphone() as source:
        audio=input.listen(source)
        data=""
        try:
            data=input.recognize_google(audio)
            print("Your question is, " + data)
            
        except sr.UnknownValueError:
            print("Sorry I did not hear your question, Please repeat again.")
        return data     
       


# In[ ]:


def respond(output):
    num=0
    print(output)
    num += 1
    response=gTTS(text=output, lang='en')
    file = str(num)+".mp3"
    response.save(file)
    
    playsound.playsound(file, True)  
    os.remove(file)


# In[ ]:


if __name__=='__main__':
    respond("Hi, Sir")
          
    while(1):
        
        respond("How can I help you?")
        text=talk().lower()

        cur.execute('INSERT INTO experiments (sch) values (text)')
        conn.commit()
        conn.close()        


        if text==0:
            continue
            
        if "stop" in str(text) or "exit" in str(text) or "bye" in str(text):
            respond("Ok bye and take care")
            break
            
        if 'wikipedia' in text:
            respond('Searching Wikipedia')
            text =text.replace("wikipedia", "")
            results = wikipedia.summary(text, sentences=3)
            respond("According to Wikipedia")
            print(results)
            respond(results)
                  
        elif 'time' in text:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            respond(f"the time is {strTime}")     
        
            
        elif 'search'  in text:
            text = text.replace("search", "")
            webbrowser.open_new_tab(text)
            time.sleep(5)

       # elif "camera" in statement or "take a photo" in statement:
        #    ec.capture(0,"robo camera","img.jpg")
        
            
        elif "calculate" or "what is" in text: 
                           
            question=talk()
            app_id="W6TVPU-J8VP8GLREX"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            respond("The answer is " + answer)
            
        elif 'who are you' in text or 'what can you do' in text:
            respond('I am Aannu, your personal desktop assistant. I can fetch information for you, perform mathematical calculations, take photo, open applications, get weather details,  and otherthings are developing by YC Bro developing team')

        elif 'open gmail' in text:
            webbrowser.open_new_tab("https://www.gmail.com")
            respond("Gmail is open")
            time.sleep(5)

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Mirthula")
            print("I was built by Mirthula")
        
        elif 'open google' in text:
            webbrowser.open_new_tab("https://www.google.com")
            respond("Google is open")
            time.sleep(5)
            
        elif 'youtube' in text: 
            driver = webdriver.Chrome(r"C:\Users\DhanushDhyan\Downloads\chromedriver_win32\chromedriver.exe") 
            driver.implicitly_wait(1) 
            driver.maximize_window()
  
            respond("Opening in youtube") 
            indx = text.split().index('youtube') 
            query = text.split()[indx + 1:] 
            driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query)) 
        
        elif "weather" in text:
            respond("what is the city name")
            city_name=talk()
            api_key="8dbd355c9d502e48bf10eea0e0a82deb"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                respond(" Temperature is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                
        elif "shut down" in text:
            respond("Ok , your system will shut down in 10 secs")
            subprocess.call(["shutdown", "/l"])        
        
        elif "open word" in text: 
            respond("Opening Microsoft Word") 
            os.startfile('C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.exe') 
        
        else: 
  
            respond("Application not available") 





