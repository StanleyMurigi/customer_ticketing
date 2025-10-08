import pyttsx3
import platform
import threading
import queue
import time

_tts_queue = queue.Queue()
_tts_thread = None
_stop_event = threading.Event()


def _speak_text(text: str):
    """Create a fresh engine each time to avoid SAPI5 lock issues."""
    engine = pyttsx3.init()
    system = platform.system()

    # Voice selection per platform
    if system == "Windows":
        voices = engine.getProperty("voices")
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        else:
            engine.setProperty("voice", voices[0].id)
    elif system == "Linux":
        voices = engine.getProperty("voices")
        # Try a female-sounding voice if available
        for voice in voices:
            if "female" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break

    engine.say(text)
    engine.runAndWait()
    engine.stop()


def _tts_worker():
    """Continuously process queued speech requests."""
    while not _stop_event.is_set():
        try:
            text = _tts_queue.get(timeout=1)
        except queue.Empty:
            continue
        if text is None:
            break
        try:
            _speak_text(text)
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            _tts_queue.task_done()
        time.sleep(0.1)  # Give system a small break before next voice


def tts_say(text: str):
    """Queue text for speech."""
    global _tts_thread
    if _tts_thread is None or not _tts_thread.is_alive():
        _tts_thread = threading.Thread(target=_tts_worker, daemon=True)
        _tts_thread.start()
    _tts_queue.put(text)


def tts_shutdown():
    """Cleanly stop the worker thread."""
    _stop_event.set()
    _tts_queue.put(None)
    if _tts_thread:
        _tts_thread.join()
