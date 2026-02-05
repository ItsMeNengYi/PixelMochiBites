import pyttsx3
import threading
import speech_recognition as sr
import time

class VoiceAssistant:
    def __init__(self, pace=170):
        self.pace = pace
        self._lock = threading.Lock()
        self.stop_event = threading.Event()
        self.is_speaking = False

    def _speech_worker(self, text):
        # We initialize the engine INSIDE the thread to keep it isolated
        # This is the secret to preventing macOS NSSpeech hangs
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', self.pace)
        
        self.is_speaking = True
        
        # We use a short loop or direct call
        # If stop_event is set, we don't even start
        if not self.stop_event.is_set():
            local_engine.say(text)
            local_engine.runAndWait()
        
        local_engine.stop() # Clean up local resources
        self.is_speaking = False

    def speak(self, text):
        """Interrupts and speaks without deadlocking the engine."""
        
        # 1. Signal any existing thread to stop (if they check for it)
        # and forcefully clear our speaking state
        self.stop_event.set()
        
        # 2. On Mac, we need to wait for the previous thread to acknowledge 
        # the stop or simply wait for the Lock to clear.
        with self._lock:
            self.stop_event.clear()
            print(f"🤖 AI: {text}")
            
            # Start a fresh worker
            t = threading.Thread(target=self._speech_worker, args=(text,), daemon=True)
            t.start()
            
            # Small buffer to prevent rapid-fire thread collision
            time.sleep(0.1)

    def listen_blocking(self):
        """Standard blocking listen: Stops code execution until speech is found."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio)
            except:
                return None

    def start_non_blocking_listen(self):
        """Starts a background worker that listens in parallel without freezing code."""
        m = sr.Microphone()
        with m as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        # This returns a function that stops the background listener
        self.stop_listening_fn = self.recognizer.listen_in_background(m, self._bg_callback)
        print("📡 Background listening active...")

    def _bg_callback(self, recognizer, audio):
        """Internal callback for the background worker."""
        try:
            text = recognizer.recognize_google(audio)
            print(f"👂 (BG) Heard: {text}")
            self.last_recognized_text = text
        except:
            pass

    def stop_bg_listen(self):
        """Call this to kill the background listener thread."""
        if self.stop_listening_fn:
            self.stop_listening_fn(wait_for_stop=False)
            print("🛑 Background listening stopped.")