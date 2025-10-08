import pyttsx3
import platform

def tts_say(text):
    engine = pyttsx3.init()
    system = platform.system()
    # On Windows, explicitly set a SAPI5 voice
    if system == "Windows":
        voices = engine.getProperty('voices')
        # Try to select a female voice if available
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        # If not found, just use the first available voice
        else:
            engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
