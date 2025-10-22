from gtts import gTTS, lang
import os
import subprocess
import tempfile

def speed_up_audio(input_path, speed=1.5):
    """
    Speeds up an audio file using FFmpeg and replaces the original file.
    
    Args:
        input_path (str): Path to the input audio file.
        speed (float): Speed factor (e.g., 1.5 = 1.5x faster).
    """
    # Create temporary output file in the same directory
    dir_name = os.path.dirname(input_path)
    with tempfile.NamedTemporaryFile(suffix=".mp3", dir=dir_name, delete=False) as tmp:
        temp_path = tmp.name

    # Handle valid speed ranges for FFmpeg atempo
    if speed < 0.5 or speed > 2.0:
        filters = []
        remaining = speed
        while remaining > 2.0:
            filters.append("atempo=2.0")
            remaining /= 2.0
        while remaining < 0.5:
            filters.append("atempo=0.5")
            remaining /= 0.5
        filters.append(f"atempo={remaining}")
        atempo_filter = ",".join(filters)
    else:
        atempo_filter = f"atempo={speed}"

    # Run FFmpeg command
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-filter:a", atempo_filter,
        "-vn", temp_path
    ]
    subprocess.run(cmd, check=True)

    # Replace original file
    os.replace(temp_path, input_path)
    print(f"✅ Replaced original file: {input_path}")




def create_tts(text,username,messageid,lang):
    language = "pa"  
    if lang == 1 :
        language = "fr"
    slow_speed = False  
    tts_object = gTTS(text=text, lang=language, slow=slow_speed)
    filename = "TTS/"+username+"_"+str(messageid)+".mp3"
    tts_object.save(filename)

    # speed_up_audio(filename,1.1)

    return filename

def delete_tts(url):
    os.remove(url)


