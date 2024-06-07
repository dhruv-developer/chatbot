import csv
import random
import spacy
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from AppKit import NSSpeechSynthesizer

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def read_csv(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            farm = row.pop('farm')
            data[farm] = row
    return data

def get_random_answer():
    return random.choice([
        "It's currently unknown.",
        "I'm not sure about that.",
        "Let me check...",
        "Sorry, I don't have that information.",
        "I'm unable to retrieve that data.",
        "It seems there's an issue accessing the data.",
        "I'll need more information to answer that.",
        "Could you please provide more details?",
        "I'm afraid I can't do that right now.",
        "The data for that is not available at the moment."
    ])

def record_audio(duration=5, filename="input.wav"):
    samplerate = 16000
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate,
                    channels=1, dtype='int16')
    print("Recording...")
    sd.wait()
    sf.write(filename, mydata, samplerate)
    print("Recording stopped.")

def recognize_speech():
    record_audio()  # Record audio using sounddevice
    recognizer = sr.Recognizer()
    with sr.AudioFile("input.wav") as source:
        audio = recognizer.record(source)  # Record the audio file
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Speech was unclear, please repeat."
    except sr.RequestError:
        return "Request failed; check your internet connection."

def get_answer(farm_data, question):
    doc = nlp(question.lower())
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    farm_identified = None
    for farm in farm_data.keys():
        if farm.lower() in question.lower():
            farm_identified = farm
            break
    if not farm_identified:
        return "Please specify which farm you are asking about."
    for attribute, value in farm_data[farm_identified].items():
        if any(keyword in attribute.lower() for keyword in keywords):
            return f"The {attribute} in {farm_identified} is {value}."
    return get_random_answer()

def speak_text(text):
    synthesizer = NSSpeechSynthesizer.alloc().initWithVoice_(None)
    synthesizer.startSpeakingString_(text)

def main():
    filename = 'farm_data.csv'
    farm_data = read_csv(filename)
    while True:
        print("You can type 'speak' to use voice input or 'exit' to quit.")
        command = input("Type your command: ")
        if command.lower() == "exit":
            print("Goodbye!")
            break
        elif command.lower() == "speak":
            question = recognize_speech()
            print(f"You said: {question}")
            answer = get_answer(farm_data, question)
            print(answer)
            speak_text(answer)  # Speak out the full answer
        else:
            question = command

        if question.lower() == "exit":
            print("Goodbye!")
            break
        answer = get_answer(farm_data, question)
        print(answer)
        speak_text(answer)  # Speak out the full answer

if __name__ == "__main__":
    main()
