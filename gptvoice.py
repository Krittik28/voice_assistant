import openai
import pyttsx3
import speech_recognition as sr
import time

#Set openai API key
openai.api_key="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"

#Initiate text to speech engine
engine=pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer=sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio=recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping.. Unknown error')
        
def generate_response(prompt):
    response=openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
            
def main():
    while True:
        #wait for user to say "start"
        speak_text("Hello Krittik")
        print("Say 'hello' to proceed")
        with sr.Microphone() as source:
                recognizer=sr.Recognizer()
                audio=recognizer.listen(source)
        transcription=recognizer.recognize_google(audio)
        if transcription.lower()=="hello":
            speak_text("how may I help you?")
            while True:
                try:
                    #Record audio
                    filename="input.wav"
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()    
                        source.pause_threshold=1
                        audio=recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename,"wb") as f:
                            f.write(audio.get_wav_data())
                        
                    #Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said: {text}")
                            
                        #generate response using gpt3
                        response=generate_response(text)
                        print(f"{response}")
                            
                        #read response using text to speech
                        speak_text(response)
                        
                        continue        
                except Exception as e:
                    print("An error occured: {}".format(e))
if __name__=="__main__":
    main()                         
                                        