import pyttsx3

engine = pyttsx3.init()  # Initialize TTS engine
engine.say("What is the runtime complexity of Merge-Sort?")
engine.runAndWait()  # Speak