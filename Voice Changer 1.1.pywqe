import tkinter as tk
import pyaudio
import librosa
import numpy as np
from threading import Thread
from tkinter import ttk
from tkinter import filedialog, messagebox
import os

class VoiceChangerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Changer App")
        self.root.protocol("WM_DELETE_WINDOW", self.cleanup)

        # Create audio recorder
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

        # Initialize effects
        self.effects = {"Normal": lambda x: x, 
                        "Robot": self.robot_voice, 
                        "Chipmunk": self.chipmunk_voice, 
                        "Echo": self.echo_voice}

        # Create UI elements
        self.title_label = tk.Label(self.root, text="Voice Changer App", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.effect_label = tk.Label(self.root, text="Select an Effect:", font=("Helvetica", 14))
        self.effect_label.pack()

        self.effect_combo = ttk.Combobox(self.root, values=list(self.effects.keys()), state="readonly")
        self.effect_combo.current(0)
        self.effect_combo.pack(pady=10)

        self.record_button = tk.Button(self.root, text="Record", font=("Helvetica", 14), command=self.record_audio)
        self.record_button.pack(pady=20)

        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 14), command=self.stop_audio, state="disabled")
        self.stop_button.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", font=("Helvetica", 14), command=self.play_audio, state="disabled")
        self.play_button.pack(pady=10)

        # Create options menu
        self.options_button = tk.Button(self.root, text="Options", font=("Helvetica", 14), command=self.show_options)
        self.options_button.pack(pady=10)

        # Create settings menu
        self.settings_button = tk.Button(self.root, text="Settings", font=("Helvetica", 14), command=self.show_settings)
        self.settings_button.pack(pady=10)

        # Initialize options and settings
        self.rate = tk.DoubleVar()
        self.rate.set(1.0)
        self.delay = tk.DoubleVar()
        self.delay.set(0.25)
        self.decay = tk.DoubleVar()
        self.decay.set(0.5)

        # Set up menu bar
        self.menu_bar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.cleanup)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

        # Start main loop
        self.root.mainloop()

    def robot_voice(self, audio):
        '''Converts
    Parameters:
    audio (numpy.ndarray): Input audio signal.

    Returns:
    numpy.ndarray: Processed audio signal with robotic effect.
    '''

    # Apply pitch shifting
    y_pitch_shift = librosa.effects.pitch_shift(audio, sr=44100, n_steps=2, bins_per_octave=12)

    # Apply time stretching
    y_time_stretch = librosa.effects.time_stretch(y_pitch_shift, rate=0.8)

    return y_time_stretch

def chipmunk_voice(self, audio):
    '''Converts audio input into a chipmunk voice.

    Parameters:
    audio (numpy.ndarray): Input audio signal.

    Returns:
    numpy.ndarray: Processed audio signal with chipmunk effect.
    '''

    # Apply pitch shifting
    y_pitch_shift = librosa.effects.pitch_shift(audio, sr=44100, n_steps=6, bins_per_octave=12)

    # Apply time stretching
    y_time_stretch = librosa.effects.time_stretch(y_pitch_shift, rate=1.5)

    return y_time_stretch

def echo_voice(self, audio):
    '''Adds an echo effect to the audio input.

    Parameters:
    audio (numpy.ndarray): Input audio signal.

    Returns:
    numpy.ndarray: Processed audio signal with echo effect.
    '''

    # Apply delay effect
    y_delay = librosa.effects.delay(audio, sr=44100, delay_time=self.delay.get())

    # Apply decay effect
    y_decay = librosa.effects.decay(y_delay, sr=44100, decay=self.decay.get())

    return y_decay

def record_audio(self):
    '''Starts recording audio from the microphone.'''

    # Disable record button and enable stop button
    self.record_button.config(state="disabled")
    self.stop_button.config(state="normal")

    # Start recording in separate thread
    self.recording_thread = Thread(target=self.record_thread)
    self.recording_thread.start()

def record_thread(self):
    '''Target function for recording thread.'''

    frames = []

    while True:
        data = self.stream.read(1024)
        frames.append(data)

        # Check if stop button was pressed
        if not self.recording_thread.is_alive():
            break

    # Stop recording and reset stream
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()

    # Convert frames to numpy array
    audio = np.frombuffer(b"".join(frames), dtype=np.float32)

    # Apply effect
    effect_func = self.effects[self.effect_combo.get()]
    processed_audio = effect_func(audio)

    # Save processed audio
    self.processed_audio = processed_audio

    # Enable play button
    self.play_button.config(state="normal")

def stop_audio(self):
    '''Stops recording audio from the microphone.'''

    # Enable record button and disable stop button
    self.record_button.config(state="normal")
    self.stop_button.config(state="disabled")

    # Stop recording thread
    self.recording_thread.join(timeout=1)
    if self.recording_thread.is_alive():
        self.recording_thread.stop()

    # Stop playing thread
    self.playing_thread.join(timeout=1)
    if self.playing_thread.is_alive():
        self.playing_thread.stop()

    # Reset audio stream
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()

def play_audio(self):
    '''Plays the processed audio.'''

    # Disable play button and enable stop button
    self.play_button.config(state="disabled")
    self.stop_button.config(state="normal")

    # Start playing in separate thread
    self.playing_thread = Thread(target=self
.play_thread)
self.playing_thread.start()

def play_thread(self):
'''Target function for playing thread.'''
# Create stream and play audio
self.stream = self.p.open(format=pyaudio.paFloat32,
                          channels=1,
                          rate=44100,
                          output=True)

self.stream.write(self.processed_audio.tobytes())

# Stop playing and reset stream
self.stream.stop_stream()
self.stream.close()
self.p.terminate()

# Enable record button and disable stop button
self.record_button.config(state="normal")
self.stop_button.config(state="disabled")
self.play_button.config(state="normal")

# Reset processed audio
self.processed_audio = None

def save_audio(self):
'''Saves the processed audio to a file.'''
# Get filename from user
filename = filedialog.asksaveasfilename(defaultextension=".wav",
                                        filetypes=[("Waveform Audio File Format", "*.wav")])
if filename:

    # Create wave file
    with wave.open(filename, mode="wb") as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)
        wave_file.setframerate(44100)
        wave_file.writeframes(self.processed_audio.tobytes())

    messagebox.showinfo("Save Audio", "Audio saved successfully.")

    def quit(self):
'''Quits the application.'''
# Stop recording thread
self.stop_audio()

# Stop playing thread
self.play_audio()

# Close application
self.root.destroy()
    def stop_audio(self):
        '''Stops recording audio from the microphone.'''

        # Enable record button and disable stop button
        self.record_button.config(state="normal")
        self.stop_button.config(state="disabled")

        # Stop recording thread and get recorded audio
        self.recording_thread.join()
        audio = np.frombuffer(b"".join(self.frames), dtype=np.float32)

        # Apply effect to audio and update audio output
        effect = self.effects[self.effect_combo.get()]
        processed_audio = effect(audio)
        self.stream.write(processed_audio.tobytes())

        # Enable play button
        self.play_button.config(state="normal")

    def play_audio(self):
        '''Plays the recorded audio with the selected effect.'''

        # Disable play button
        self.play_button.config(state="disabled")

        # Play audio in separate thread
        self.playback_thread = Thread(target=self.playback_thread, args=(self.effects[self.effect_combo.get()],))
        self.playback_thread.start()

    def playback_thread(self, effect):
        '''Target function for playback thread.'''

        # Apply effect to audio and play audio
        processed_audio = effect(np.frombuffer(b"".join(self.frames), dtype=np.float32))
        self.stream.write(processed_audio.tobytes())

        # Enable play button
        self.play_button.config(state="normal")

    def show_options(self):
        '''Displays the options menu.'''

        # Create options window
        self.options_window = tk.Toplevel(self.root)
        self.options_window.title("Options")
        self.options_window.transient(self.root)
        self.options_window.grab_set()

        # Create options frame
        self.options_frame = ttk.Frame(self.options_window)
        self.options_frame.pack(padx=20, pady=20)

        # Create rate slider
        rate_label = ttk.Label(self.options_frame, text="Rate")
        rate_label.pack()
        rate_slider = ttk.Scale(self.options_frame, from_=0.5, to=2.0, variable=self.rate, orient=tk.HORIZONTAL, length=200, command=self.update_options_label)
        rate_slider.pack()
        self.update_options_label(None, None, None)

        # Create OK button
        ok_button = ttk.Button(self.options_window, text="OK", command=self.hide_options)
        ok_button.pack(pady=10)

    def update_options_label(self, event, widget, value):
        '''Updates the label for the rate slider in the options menu.'''

        rate_label_text = f"Rate: {self.rate.get():.2f}"
        self.options_window.children["!label"].config(text=rate_label_text)

    def hide_options(self):
        '''Hides the options menu.'''

        self.options_window.destroy()

    def show_settings(self
    # Create settings window
    self.settings_window = tk.Toplevel(self.root)
    self.settings_window.title("Settings")
    self.settings_window.transient(self.root)
    self.settings_window.grab_set()

    # Create settings frame
    self.settings_frame = ttk.Frame(self.settings_window)
    self.settings_frame.pack(padx=20, pady=20)

    # Create effect combo box
    effect_label = ttk.Label(self.settings_frame, text="Effect")
    effect_label.pack()
    self.effect_combo = ttk.Combobox(self.settings_frame, values=list(self.effects.keys()))
    self.effect_combo.pack()
    self.effect_combo.set("None")

    # Create OK button
    ok_button = ttk.Button(self.settings_window, text="OK", command=self.hide_settings)
    ok_button.pack(pady=10)

def hide_settings(self):
    '''Hides the settings menu.'''

    self.settings_window.destroy()

def show_about(self):
    '''Displays the about dialog.'''

    # Create about window
    self.about_window = tk.Toplevel(self.root)
    self.about_window.title("About")
    self.about_window.transient(self.root)
    self.about_window.grab_set()

    # Create about frame
    self.about_frame = ttk.Frame(self.about_window)
    self.about_frame.pack(padx=20, pady=20)

    # Create about text
    about_text = ttk.Label(self.about_frame, text="This is a simple audio recorder application using Python and Tkinter.")
    about_text.pack()

    # Create OK button
    ok_button = ttk.Button(self.about_window, text="OK", command=self.hide_about)
    ok_button.pack(pady=10)

def hide_about(self):
    '''Hides the about dialog.'''

    self.about_window.destroy()
if name == "main":
app = AudioRecorder()
app.run()
                              if not self.recording_thread.is_alive():
            break

    # Stop recording and enable play button
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    self.audio_data = b''.join(frames)
    self.play_button.config(state="normal")

def stop_audio(self):
    '''Stops recording or playing audio.'''

    # Stop recording or playing and enable record button
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    self.record_button.config(state="normal")
    self.stop_button.config(state="disabled")
    self.play_button.config(state="normal")

def play_audio(self):
    '''Plays back the recorded audio with the selected effect.'''

    # Disable play button
    self.play_button.config(state="disabled")

    # Apply effect to audio
    effect_name = self.effect_combo.get()
    effect_func = self.effects[effect_name]
    audio, sr = librosa.load(self.audio_data, sr=44100, mono=True)
    processed_audio = effect_func(audio)

    # Play back audio
    self.play_thread = Thread(target=self.play_thread, args=(processed_audio,))
    self.play_thread.start()

def play_thread(self, audio):
    '''Target function for playback thread.'''

    self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=False, output=True)
    self.stream.write(audio.tobytes())
    self.stream.close()
    self.p.terminate()
    self.play_button.config(state="normal")

def show_options(self):
    '''Displays the options menu.'''

    # Create options window
    self.options_window = tk.Toplevel(self.root)
    self.options_window.title("Options")

    # Create options label and entry for rate
    rate_label = tk.Label(self.options_window, text="Rate:")
    rate_label.grid(row=0, column=0, padx=10, pady=10)
    rate_entry = tk.Entry(self.options_window, textvariable=self.rate)
    rate_entry.grid(row=0, column=1, padx=10, pady=10)

    # Create options label and entry for delay
    delay_label = tk.Label(self.options_window, text="Delay (s):")
    delay_label.grid(row=1, column=0, padx=10, pady=10)
    delay_entry = tk.Entry(self.options_window, textvariable=self.delay)
    delay_entry.grid(row=1, column=1, padx=10, pady=10)

    # Create options label and entry for decay
    decay_label = tk.Label(self.options_window, text="Decay:")
    decay_label.grid(row=2, column=0, padx=10, pady=10)
    decay_entry = tk.Entry(self.options_window, textvariable=self.decay)
    decay_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create apply button
    apply_button = tk.Button(self.options_window, text="Apply", command=self.apply_options)
    apply_button.grid(row=3, column=0, columnspan=2, pady=10)

def apply_options(self):
    '''Applies the options set in the options menu.'''

    # Close options window
    self.options_window.destroy()

def show_settings(self):
    '''Displays the settings menu.'''

    # Create settings window
    self.settings_window = tk.Toplevel(self.root)
    self.settings_window.title("Settings")

    # Create settings label and button for changing directory
    directory_label = tk.Label(self.settings_window, text="Directory:")
    directory_label.grid(row=0, column=0, padx=10,
def stop_audio(self):
    '''Stops recording audio from the microphone.'''

    # Disable stop button and enable play button
    self.stop_button.config(state="disabled")
    self.play_button.config(state="normal")

    # Stop recording
    self.recording = False

def play_audio(self):
    '''Plays back the recorded audio with the selected effect applied.'''

    # Disable play button
    self.play_button.config(state="disabled")

    # Apply selected effect to audio
    effect_name = self.effect_combo.get()
    effect_func = self.effects[effect_name]
    audio = np.array(self.audio_frames)
    audio_processed = effect_func(audio)

    # Play audio in separate thread
    self.play_thread = Thread(target=self.play_thread, args=(audio_processed,))
    self.play_thread.start()

def play_thread(self, audio):
    '''Target function for audio playback thread.'''

    # Open audio stream for playback
    stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

    # Play audio
    stream.write(audio)

    # Clean up
    stream.stop_stream()
    stream.close()
    self.p.terminate()

def cleanup(self):
    '''Cleans up resources and closes the application.'''

    # Stop recording if it is in progress
    self.recording = False
    if hasattr(self, "recording_thread"):
        self.recording_thread.join()

    # Terminate audio stream
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()

    # Close the application
    self.root.destroy()

def show_options(self):
    '''Displays the options dialog.'''

    # Create options dialog
    self.options_dialog = tk.Toplevel(self.root)
    self.options_dialog.title("Options")

    # Create rate slider
    rate_label = tk.Label(self.options_dialog, text="Rate:")
    rate_label.grid(row=0, column=0)
    rate_slider = tk.Scale(self.options_dialog, from_=0.5, to=1.5, resolution=0.01, orient="horizontal", variable=self.rate)
    rate_slider.grid(row=0, column=1)

    # Create delay slider
    delay_label = tk.Label(self.options_dialog, text="Delay:")
    delay_label.grid(row=1, column=0)
    delay_slider = tk.Scale(self.options_dialog, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", variable=self.delay)
    delay_slider.grid(row=1, column=1)

    # Create decay slider
    decay_label = tk.Label(self.options_dialog, text="Decay:")
    decay_label.grid(row=2, column=0)
    decay_slider = tk.Scale(self.options_dialog, from_=0.0, to=1.0, resolution=0.01, orient="horizontal", variable=self.decay)
    decay_slider.grid(row=2, column=1)

    # Create OK button
    ok_button = tk.Button(self.options_dialog, text="OK", font=("Helvetica", 14), command=self.options_ok)
    ok_button.grid(row=3, column=1)

def options_ok(self):
    '''Updates settings based on options dialog and closes the dialog.'''

    # Update settings
    self.rate.set(round(self.rate.get(), 2))
    self.delay.set(round(self.delay.get(), 2))
    self.decay.set(round(self.decay.get(), 2))

    # Close options dialog
    self.options_dialog.destroy()

def show_settings(self):
    '''Displays the settings dialog.'''

   
def show_settings(self):
    '''Displays the settings dialog.'''

    # Create settings dialog
    self.settings_dialog = tk.Toplevel(self.root)
    self.settings_dialog.title("Settings")

    # Create effect selection label and combo box
    effect_label = tk.Label(self.settings_dialog, text="Effect:")
    effect_label.grid(row=0, column=0)
    self.effect_combo = ttk.Combobox(self.settings_dialog, values=list(self.effects.keys()))
    self.effect_combo.current(0)
    self.effect_combo.grid(row=0, column=1)

    # Create input device selection label and combo box
    input_label = tk.Label(self.settings_dialog, text="Input:")
    input_label.grid(row=1, column=0)
    self.input_combo = ttk.Combobox(self.settings_dialog, values=self.get_input_devices())
    self.input_combo.current(0)
    self.input_combo.grid(row=1, column=1)

    # Create output device selection label and combo box
    output_label = tk.Label(self.settings_dialog, text="Output:")
    output_label.grid(row=2, column=0)
    self.output_combo = ttk.Combobox(self.settings_dialog, values=self.get_output_devices())
    self.output_combo.current(0)
    self.output_combo.grid(row=2, column=1)

    # Create OK button
    ok_button = tk.Button(self.settings_dialog, text="OK", font=("Helvetica", 14), command=self.settings_ok)
    ok_button.grid(row=3, column=1)

def settings_ok(self):
    '''Updates settings based on settings dialog and closes the dialog.'''

    # Update effect
    effect_name = self.effect_combo.get()
    self.selected_effect = effect_name

    # Update input device
    input_device_index = self.input_combo.current()
    self.input_device_index = input_device_index

    # Update output device
    output_device_index = self.output_combo.current()
    self.output_device_index = output_device_index

    # Close settings dialog
    self.settings_dialog.destroy()

def get_input_devices(self):
    '''Returns a list of available input devices.'''

    device_count = self.p.get_device_count()
    devices = []
    for i in range(device_count):
        device_info = self.p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            devices.append(device_info["name"])
    return devices

def get_output_devices(self):
    '''Returns a list of available output devices.'''

    device_count = self.p.get_device_count()
    devices = []
    for i in range(device_count):
        device_info = self.p.get_device_info_by_index(i)
        if device_info["maxOutputChannels"] > 0:
            devices.append(device_info["name"])
    return devices
while True:
    try:
        choice = int(input("Enter your choice: "))
        break
    except ValueError:
        print("Invalid input. Please enter a number.")
