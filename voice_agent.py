import pyttsx3
import threading
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.recognizer = sr.Recognizer()

    def _speech_worker(self, text):
        """Internal worker to handle the blocking runAndWait call."""
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

    def speak_interrupt(self, text):
        """Interrupts current speech and starts new speech immediately."""
        if self.is_speaking:
            # This clears the current command queue in pyttsx3
            self.engine.stop()
            print("🛑 Interrupted current speech.")
        
        # Start a new thread for the new text so it doesn't block your main app
        threading.Thread(target=self._speech_worker, args=(text,), daemon=True).start()

    def speak(self, text):
            """Convert text to audible speech."""
            print(f"🤖 AI: {text}")
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self):
        """Standard listen function."""
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                return self.recognizer.recognize_google(audio)
            except:
                return None
    def listen_blocking(self):
        """
        Blocks execution until a valid command is recognized.
        Retries automatically on silence or errors.
        """
        while True:
            with sr.Microphone() as source:
                print("\n🎤 Waiting for command...")
                # Adjust for noise every loop to stay calibrated
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    # phrase_time_limit prevents it from listening forever if noise is constant
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    print("🔍 Transcribing...")
                    
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        print(f"✅ Recognized: {text}")
                        return text # Exit the loop and return result
                
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    # Silent or garbled audio, just loop back
                    continue
                except sr.RequestError:
                    print("🌐 Network error. Check connection.")
                    return None
# --- Example of Interruption ---i
if __name__ == "__main__":
    va = VoiceAssistant()
    va.speak("Voice system active.")
    while True:
        cmd = va.listen_blocking()
        if cmd:
            va.speak(f"You said {cmd}")