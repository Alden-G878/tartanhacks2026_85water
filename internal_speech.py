import speech_recognition as sr

def get_speech():
    
    # Initialize the recognizer
    r = sr.Recognizer()
    
    # Use the microphone as source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        # Adjust for ambient noise for better accuracy (optional)
        r.adjust_for_ambient_noise(source, duration=1) 
        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
    
    try:
        # Use Google Web Speech API for recognition
        text = r.recognize_google(audio)
        print("Recognized!")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

