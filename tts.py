import pyttsx3
import platform
import threading
import queue

_tts_queue = queue.Queue()
_tts_thread = None

def _tts_worker():
    engine = pyttsx3.init()
    system = platform.system()
    if system == "Windows":
        voices = engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        else:
            engine.setProperty('voice', voices[0].id)
    while True:
        text = _tts_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()

def tts_say(text):
    global _tts_thread
    if _tts_thread is None or not _tts_thread.is_alive():
        _tts_thread = threading.Thread(target=_tts_worker, daemon=True)
        _tts_thread.start()
    _tts_queue.put(text)
