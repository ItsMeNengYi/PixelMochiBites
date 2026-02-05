import pyttsx3
import threading
import speech_recognition as sr
import time

class VoiceAssistant:
    def __init__(self, pace=170):
        # We don't use a global engine for speaking anymore to prevent Mac hangs
        self.pace = pace
        self.recognizer = sr.Recognizer()
        self._active_threads = 0
        self._counter_lock = threading.Lock()
        self.muted = False
        self.mic_muted = False
        self.callback = None
        self.stop_listening_fn = None

    @property
    def is_speaking(self):
        """Dynamic check: Returns True only if threads are actively registered."""
        with self._counter_lock:
            # We use a safety check to ensure count never goes below 0
            return self._active_threads > 0

    def _speech_worker(self, text):
        try:
            # Re-init is necessary for Mac/pyenv stability
            local_engine = pyttsx3.init()
            local_engine.setProperty('rate', self.pace)
            
            local_engine.say(text)
            local_engine.runAndWait()
            
            local_engine.stop()
            del local_engine
        except Exception as e:
            print(f"❌ Worker Error: {e}")
        finally:
            # DECREMENT: Wrap in try/finally to ensure the count ALWAYS drops
            with self._counter_lock:
                if self._active_threads > 0:
                    self._active_threads -= 1
                print(f"📉 Voice finished. Remaining: {self._active_threads}")

    def speak(self, text):
        if self.muted or not text:
            return

        # INCREMENT: Ensure the 'True' state is locked before the thread even begins
        with self._counter_lock:
            self._active_threads += 1
            print(f"📈 Voice started. Active: {self._active_threads}")

        t = threading.Thread(target=self._speech_worker, args=(text,), daemon=True)
        t.start()
    
    def listen_blocking(self):
        if self.mic_muted:
            return None
        """Standard blocking listen: Stops code execution until speech is found."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio)
            except:
                return None

    def start_non_blocking_listen(self, callback=None):
        if self.mic_muted:
            return
        """Starts a background worker that listens in parallel without freezing code."""
        self.callback = callback
        
        m = sr.Microphone()
        with m as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        # This returns a function that stops the background listener
        self.stop_listening_fn = self.recognizer.listen_in_background(m, self._bg_callback)
        print("📡 Background listening active...")

    def _bg_callback(self, recognizer, audio):
        """Internal callback for the background worker."""
        print("IS SPEAKING:", self.is_speaking)
        if self.is_speaking:
            return
        try:
            text = recognizer.recognize_google(audio)
            print(f"👂 (BG) Heard: {text}")
            if self.callback:
                self.callback(text)
        except:
            pass

    def stop_bg_listen(self):
        """Call this to kill the background listener thread."""
        if self.stop_listening_fn:
            self.stop_listening_fn(wait_for_stop=False)
            print("🛑 Background listening stopped.")

    def mute(self):
        self.muted = True
    
    def mute_mic(self):
        self.stop_bg_listen()
        self.mic_muted = True
        
    def unmute(self):
        self.muted = False
    
    def unmute_mic(self):
        self.mic_muted = False