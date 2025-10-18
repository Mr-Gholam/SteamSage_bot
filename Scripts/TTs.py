from gtts import gTTS, lang
import os
import subprocess



def create_tts(text,username,messageid):
    language = "pa"  
    slow_speed = False  
    tts_object = gTTS(text=text, lang=language, slow=slow_speed)
    filename = "TTS/"+username+"_"+str(messageid)+".mp3"
    tts_object.save(filename)

    return filename

def delete_tts(url):
    os.remove(url)
