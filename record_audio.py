import sounddevice as sd
import speech_recognition as sr
import numpy as np
import wave
import tkinter as tk
from tkinter import messagebox
import threading

# Parameters
RATE = 44100  # Sample rate (Hz)
CHANNELS = 1  # Mono
FILENAME = "output.wav"  # Output file name

# Global variables for controlling recording
recording = False
audio_data = []

# Function to start recording
def start_recording(event):
    global recording, audio_data
    if not recording:
        print("Recording started...")
        recording = True
        audio_data = []
        
        # Record audio in chunks
        def record():
            with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16') as stream:
                while recording:
                    # Read audio data in chunks and append to the audio data list
                    chunk, overflowed = stream.read(RATE)
                    audio_data.append(chunk)

        # Start recording in a separate thread
        threading.Thread(target=record, daemon=True).start()

# Function to stop recording
def stop_recording(event):
    global recording, audio_data
    if recording:
        recording = False
        print("Recording stopped.")
        
        # Save the recorded data to a file
        audio_data = np.concatenate(audio_data, axis=0)
        with wave.open(FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 2 bytes (16 bits per sample)
            wf.setframerate(RATE)
            wf.writeframes(audio_data.tobytes())
        
        print(f"Audio saved to {FILENAME}")
        messagebox.showinfo("Success", f"Recording finished. Audio saved to {FILENAME}")
    else:
        messagebox.showwarning("No Recording", "No recording is in progress.")

import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

# Path to the saved audio file
AUDIO_FILE = "output.wav"

# Function to convert speech to text
def convert_audio_to_text():
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(AUDIO_FILE) as source:
        # Adjust for ambient noise and record the audio
        audio = recognizer.record(source)

    try:
        # Recognize the speech using Google's free API (no internet required for offline recognition)
        text = recognizer.recognize_google(audio)
        print("Recognized text:", text)
        messagebox.showinfo("Speech Recognition", f"Recognized text: {text}")
    except sr.UnknownValueError:
        messagebox.showwarning("Error", "Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

# Create the GUI
root = tk.Tk()
root.title("Audio Recorder & Speech Recognition")

# Create a button to start recording
start_button = tk.Button(root, text="Hold to Record", height=2, width=20)
start_button.bind("<ButtonPress-1>", start_recording)
start_button.bind("<ButtonRelease-1>", stop_recording)
start_button.pack(pady=20)

# Create a button to convert audio to text
convert_button = tk.Button(root, text="Convert Audio to Text", command=convert_audio_to_text, height=2, width=20)
convert_button.pack(pady=20)

# Run the GUI loop
root.mainloop()

