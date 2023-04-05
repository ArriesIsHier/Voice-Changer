import os
import subprocess
import time
import threading
from queue import Queue
from scipy.io import wavfile
import numpy as np
import sounddevice as sd
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
import librosa
import librosa.display
import matplotlib.pyplot as plt
from tkinter import ttk

Install required packages if necessary
def check_packages():
packages = ['numpy', 'sounddevice', 'soundfile', 'scipy', 'matplotlib', 'librosa']
installed = subprocess.check_output(['pip', 'freeze'])
installed_packages = [pkg.decode().split('==')[0] for pkg in installed.split()]

go
Copy code
for package in packages:
    if package not in installed_packages:
        print(f'{package} not found. Installing...')
        subprocess.check_call(['pip', 'install', package])
Voice changer class
class VoiceChanger:
def init(self):
self.window = tk.Tk()
self.window.title("Voice Changer")
self.window.attributes("-fullscreen", True)
self.window.configure(background='white')
self.window.grid_rowconfigure(0, weight=1)
self.window.grid_columnconfigure(0, weight=1)
self.window.grid_columnconfigure(1, weight=1)

python
Copy code
    self.left_frame = tk.Frame(self.window, bg='white')
    self.left_frame.grid(row=0, column=0, sticky='nsew')
    self.left_frame.grid_rowconfigure(0, weight=1)
    self.left_frame.grid_columnconfigure(0, weight=1)
    self.left_frame.grid_columnconfigure(1, weight=1)
    self.left_frame.grid_columnconfigure(2, weight=1)

    self.right_frame = tk.Frame(self.window, bg='white')
    self.right_frame.grid(row=0, column=1, sticky='nsew')
    self.right_frame.grid_rowconfigure(0, weight=1)
    self.right_frame.grid_columnconfigure(0, weight=1)

    self.input_file_path = ""
    self.output_file_path = ""
    self.input_data = []
    self.input_sample_rate = 0
    self.output_sample_rate = 0
    self.output_data = []
    self.notes = []
    self.play_thread = None
    self.playing = False
    self.plot_thread = None
    self.plotting = False

    self.header_label = tk.Label(self.left_frame, text="Voice Changer", font=('Arial', 24), bg='white')
    self.header_label.grid(row=0, column=0, columnspan=3, pady=20)

    self.file_select_button = tk.Button(self.left_frame, text="Select File", font=('Arial', 16), command=self.select_file)
    self.file_select_button.grid(row=1, column=0, pady=10)

    self.output_path_label = tk.Label(self.left_frame, text="", font=('Arial', 12), bg='white')
    self.output_path_label.grid(row=2, column=0, columnspan=3, pady=10)

    self.pitch_shift_label = tk.Label(self.left_frame, text="Pitch shift (semitones):", font=('Arial', 16), bg='white')
    self.pitch_shift_label.grid(row=3, column=0, pady=10)
    self.pitch_shift = tk.Entry(self.left_frame, font=('Arial', 14))
    self.pitch_shift.grid(row=3, column=1, pady=10)

    self.speed_scale_label = tk.Label(self.left_frame, text="Speed scale (0.5-2.0):", font=('Arial', 16), bg='white')
    self.speed_scale
    self.speed_scale_label.grid(row=4, column=0, pady=10)
self.speed_scale = tk.Entry(self.left_frame, font=('Arial', 14))
self.speed_scale.grid(row=4, column=1, pady=10)

self.effect_label = tk.Label(self.left_frame, text="Select effect:", font=('Arial', 16), bg='white')
self.effect_label.grid(row=5, column=0, pady=10)
self.effect_choice = ttk.Combobox(self.left_frame, values=["None", "Echo", "Reverb", "Chorus"], font=('Arial', 14))
self.effect_choice.current(0)
self.effect_choice.grid(row=5, column=1, pady=10)

self.notes_label = tk.Label(self.left_frame, text="Notes:", font=('Arial', 16), bg='white')
self.notes_label.grid(row=6, column=0, pady=10)
self.notes_entry = tk.Entry(self.left_frame, font=('Arial', 14))
self.notes_entry.grid(row=6, column=1, pady=10)

self.play_button = tk.Button(self.left_frame, text="Play", font=('Arial', 16), command=self.play)
self.play_button.grid(row=7, column=0, pady=10)

self.plot_button = tk.Button(self.left_frame, text="Plot", font=('Arial', 16), command=self.plot)
self.plot_button.grid(row=7, column=1, pady=10)

self.save_button = tk.Button(self.left_frame, text="Save As", font=('Arial', 16), command=self.save_as)
self.save_button.grid(row=7, column=2, pady=10)

self.close_button = tk.Button(self.left_frame, text="Close", font=('Arial', 16), command=self.window.destroy)
self.close_button.grid(row=8, column=0, pady=10, columnspan=3)

self.status_label = tk.Label(self.right_frame, text="", font=('Arial', 16), bg='white')
self.status_label.grid(row=0, column=0, pady=20, padx=20)
File selection method
def select_file(self):
self.input_file_path = filedialog.askopenfilename()
self.output_file_path = os.path.splitext(self.input_file_path)[0] + "_out.wav"
self.output_path_label.configure(text="Output File: " + self.output_file_path)

Pitch shifting method
def pitch_shift(self, data, semitones):
return librosa.effects.pitch_shift(data, sr=self.input_sample_rate, n_steps=semitones)

Speed scaling method
def speed_scale(self, data, factor):
return librosa.effects.time_stretch(data, factor)

Effect methods
def echo(self, data):
return librosa.effects.echo(data, self.input_sample_rate)

def reverb(self, data):
return librosa.effects.reverb(data, self.input_sample_rate)

def chorus(self, data):
return librosa.effects.chorus(data, self.input_sample_rate)

Play method
def play(self):
if self.playing:
return
self.playing = True
self.play_thread = threading.Thread(target=self.play_thread_function)
self.play_thread.start()

Plot method
def plot(self):
if self.plotting:
return
self.plotting = True
self.plot_thread = threading.Thread(target=self.plot_thread_function)
self.plot_thread.start()

Save method
def save_as(self):
sf.write(self.output_file_path, self.output_data, self.output_sample_rate)
self
Thread functions
def play_thread_function(self):
self.status_label.configure(text="Playing...", fg='green')
self.play_button.configure(state='disabled')
self.plot_button.configure(state='disabled')
self.save_button.configure(state='disabled')
self.close_button.configure(state='disabled')
try:
with sf.SoundFile(self.output_file_path) as file:
with sd.OutputStream(channels=file.channels, samplerate=file.samplerate):
for data in file:
sd.wait()
except Exception as e:
self.status_label.configure(text="Error: " + str(e), fg='red')
finally:
self.playing = False
self.play_button.configure(state='normal')
self.plot_button.configure(state='normal')
self.save_button.configure(state='normal')
self.close_button.configure(state='normal')
self.status_label.configure(text="")

def plot_thread_function(self):
self.status_label.configure(text="Plotting...", fg='green')
self.play_button.configure(state='disabled')
self.plot_button.configure(state='disabled')
self.save_button.configure(state='disabled')
self.close_button.configure(state='disabled')
try:
plt.figure(figsize=(10, 4))
plt.plot(self.output_data)
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.title("Audio Signal")
plt.grid(True)
plt.show()
except Exception as e:
self.status_label.configure(text="Error: " + str(e), fg='red')
finally:
self.plotting = False
self.play_button.configure(state='normal')
self.plot_button.configure(state='normal')
self.save_button.configure(state='normal')
self.close_button.configure(state='normal')
self.status_label.configure(text="")

Effect selection method
def select_effect(self, event):
effect = self.effect_choice.get()
if effect == "None":
self.effect_method = None
elif effect == "Echo":
self.effect_method = self.echo
elif effect == "Reverb":
self.effect_method = self.reverb
elif effect == "Chorus":
self.effect_method = self.chorus

Processing method
def process(self):
self.status_label.configure(text="Processing...", fg='green')
self.play_button.configure(state='disabled')
self.plot_button.configure(state='disabled')
self.save_button.configure(state='disabled')
self.close_button.configure(state='disabled')
try:
self.input_data, self.input_sample_rate = librosa.load(self.input_file_path, sr=None, mono=True)
if self.pitch_shift_scale.get() != 0:
self.output_data = self.pitch_shift(self.input_data, self.pitch_shift_scale.get())
elif self.speed_scale.get() != '':
self.output_data = self.speed_scale(self.input_data, float(self.speed_scale.get()))
else:
self.output_data = self.input_data
if self.effect_method is not None:
self.output_data = self.effect_method(self.output_data)
self.output_sample_rate = self.input_sample_rate
sf.write(self.output_file_path, self.output_data, self.output_sample_rate)
self.status_label.configure(text="Finished processing.", fg='green')
except Exception as e:
self.status_label.configure(text="Error: " + str(e), fg='red')
finally:
self.play_button.configure(state='normal')
self.plot_button.configure(state='normal')
self.save_button.configure(state='normal')
self.close_button.configure(state='normal')

Initialization
def init(self):
self.window = tk.Tk()
self.window.title("Audio Processor")
self.window.configure(background='white')
self.window.geometry("800x500")

self.input_file_path = ''
self.output_file_path = ''
self.input_data = None
self.input_sample_rate = None
self.output_data = None
self.output_sample_rate = None
self.effect_method = None

self.playing = False
self.plotting = False

self.left_frame = tk.Frame(self.window, bg='white')
self.left_frame.pack
Button functions
def open_file_dialog(self):
file_path = filedialog.askopenfilename()
if file_path:
self.input_file_path = file_path
self.input_file_label.configure(text="Selected file: " + self.input_file_path)

def save_file_dialog(self):
file_path = filedialog.asksaveasfilename(defaultextension=".wav")
if file_path:
self.output_file_path = file_path
self.output_file_label.configure(text="Selected file: " + self.output_file_path)

def play_button_pressed(self):
if not self.playing:
self.playing = True
play_thread = threading.Thread(target=self.play_thread_function)
play_thread.start()

def plot_button_pressed(self):
if not self.plotting:
self.plotting = True
plot_thread = threading.Thread(target=self.plot_thread_function)
plot_thread.start()

def process_button_pressed(self):
process_thread = threading.Thread(target=self.process)
process_thread.start()

def close_button_pressed(self):
self.window.destroy()

Effect methods
def echo(self, data, delay, decay):
n = int(delay * self.output_sample_rate)
echoed_data = np.zeros_like(data)
echoed_data[n:] = data[:-n]
echoed_data = data + decay * echoed_data
return np.clip(echoed_data, -1, 1)

def reverb(self, data, room_size, decay):
comb_filter_lengths = [int(2 ** (i / 2) * room_size * self.output_sample_rate) for i in range(5)]
comb_filters = [np.zeros(length) for length in comb_filter_lengths]
comb_filter_gains = [decay ** (i + 1) for i in range(5)]
allpass_filter_lengths = [int(length / 2) for length in comb_filter_lengths]
allpass_filters = [np.zeros(length) for length in allpass_filter_lengths]
for i in range(5):
comb_filters[i][:comb_filter_lengths[i] - 1] = data
allpass_input = sum(comb_filters)
for i in range(4):
allpass_filters[i], allpass_input = self.allpass(allpass_input, allpass_filter_lengths[i])
reverberated_data = sum(comb_filters) + sum(allpass_filters)
reverberated_data /= np.max(np.abs(reverberated_data))
return np.clip(reverberated_data, -1, 1)

def chorus(self, data, depth, rate, feedback):
n = int(depth * self.output_sample_rate)
modulation = np.zeros_like(data)
for i in range(n, len(data)):
modulation[i] = data[i - n]
modulation *= feedback
modulation += data
modulation = self.pitch_shift(modulation, rate)
return np.clip(modulation, -1, 1)

Utility methods
def allpass(self, data, length):
allpass_filter = np.zeros(length)
allpass_filter[0] = 1
allpass_filter[-1] = -0.5
allpass_output = np.convolve(data, allpass_filter, mode='same')
allpass_output[1:] += allpass_output[:-1] * 0.5
allpass_output[0] *= 0.5
return allpass_output, allpass_output

def pitch_shift(self, data, shift):
return librosa.effects.pitch_shift(data, self.input_sample_rate, shift)

def speed_scale(self, data, scale):
return librosa.effects.time_stretch(data, scale)

User interface
def create_user_interface(self):
self.input_file_label = tk.Label(self.left_frame, text="No file selected.", bg='white')
self.input_file_label.pack(pady=10)
self.input_file_button = tk.Button(self.left_frame, text="
                                   from tkinter import *
from tkinter import ttk, filedialog
import threading
import librosa
import numpy as np

class AudioProcessor:
    def __init__(self):
        self.input_file_path = None
        self.output_file_path = None
        self.input_sample_rate = None
        self.output_sample_rate = 44100
        self.playing = False
        self.plotting = False

    # Button functions
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text="Selected file: " + self.input_file_path)

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav")
        if file_path:
            self.output_file_path = file_path
            self.output_file_label.configure(text="Selected file: " + self.output_file_path)

    def play_button_pressed(self):
        if not self.playing:
            self.playing = True
            play_thread = threading.Thread(target=self.play_thread_function)
            play_thread.start()

    def plot_button_pressed(self):
        if not self.plotting:
            self.plotting = True
            plot_thread = threading.Thread(target=self.plot_thread_function)
            plot_thread.start()

    def process_button_pressed(self):
        process_thread = threading.Thread(target=self.process)
        process_thread.start()

    def close_button_pressed(self):
        self.window.destroy()

    # Effect methods
    def echo(self, data, delay, decay):
        n = int(delay * self.output_sample_rate)
        echoed_data = np.zeros_like(data)
        echoed_data[n:] = data[:-n]
        echoed_data = data + decay * echoed_data
        return np.clip(echoed_data, -1, 1)

    def reverb(self, data, room_size, decay):
        comb_filter_lengths = [int(2 ** (i / 2) * room_size * self.output_sample_rate) for i in range(5)]
        comb_filters = [np.zeros(length) for length in comb_filter_lengths]
        comb_filter_gains = [decay ** (i + 1) for i in range(5)]
        allpass_filter_lengths = [int(length / 2) for length in comb_filter_lengths]
        allpass_filters = [np.zeros(length) for length in allpass_filter_lengths]
        for i in range(5):
            comb_filters[i][:comb_filter_lengths[i] - 1] = data
        allpass_input = sum(comb_filters)
        for i in range(4):
            allpass_filters[i], allpass_input = self.allpass(allpass_input, allpass_filter_lengths[i])
        reverberated_data = sum(comb_filters) + sum(allpass_filters)
        reverberated_data /= np.max(np.abs(reverberated_data))
        return np.clip(reverberated_data, -1, 1)

    def chorus(self, data, depth, rate, feedback):
        n = int(depth * self.output_sample_rate)
        modulation = np.zeros_like(data)
        for i in range(n, len(data)):
            modulation[i] = data[i - n]
        modulation *= feedback
        modulation += data
        modulation = self.pitch_shift(modulation, rate)
        return np.clip(modulation, -1, 1)

    # Utility methods
    def allpass(self, data, length):
        allpass_filter = np.zeros(length)
        allpass_filter[0] = 1
        allpass_filter[-1] = -0.5
        allpass_output = np.convolve(data, allpass_filter, mode
class AudioProcessor:
    def __init__(self):
        self.input_file_path = None
        self.output_file_path = None
        self.input_sample_rate = None
        self.output_sample_rate = 44100
        self.playing = False
        self.plotting = False

    # Button functions
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text="Selected file: " + self.input_file_path)

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav")
        if file_path:
            self.output_file_path = file_path
            self.output_file_label.configure(text="Selected file: " + self.output_file_path)

    def play_button_pressed(self):
        if not self.playing:
            self.playing = True
            play_thread = threading.Thread(target=self.play_thread_function)
            play_thread.start()

    def plot_button_pressed(self):
        if not self.plotting:
            self.plotting = True
            plot_thread = threading.Thread(target=self.plot_thread_function)
            plot_thread.start()

    def process_button_pressed(self):
        process_thread = threading.Thread(target=self.process)
        process_thread.start()

    def close_button_pressed(self):
        self.window.destroy()

    # Effect methods
    def echo(self, data, delay, decay):
        n = int(delay * self.output_sample_rate)
        echoed_data = np.zeros_like(data)
        echoed_data[n:] = data[:-n]
        echoed_data = data + decay * echoed_data
        return np.clip(echoed_data, -1, 1)

    def reverb(self, data, room_size, decay):
        comb_filter_lengths = [int(2 ** (i / 2) * room_size * self.output_sample_rate) for i in range(5)]
        comb_filters = [np.zeros(length) for length in comb_filter_lengths]
        comb_filter_gains = [decay ** (i + 1) for i in range(5)]
        allpass_filter_lengths = [int(length / 2) for length in comb_filter_lengths]
        allpass_filters = [np.zeros(length) for length in allpass_filter_lengths]
        for i in range(5):
            comb_filters[i][:comb_filter_lengths[i] - 1] = data
        allpass_input = sum(comb_filters)
        for i in range(4):
            allpass_filters[i], allpass_input = self.allpass(allpass_input, allpass_filter_lengths[i])
        reverberated_data = sum(comb_filters) + sum(allpass_filters)
        reverberated_data /= np.max(np.abs(reverberated_data))
        return np.clip(reverberated_data, -1, 1)

    def chorus(self, data, depth, rate, feedback):
        n = int(depth * self.output_sample_rate)
        modulation = np.zeros_like(data)
        for i in range(n, len(data)):
            modulation[i] = data[i - n]
        modulation *= feedback
        modulation += data
        modulation = self.pitch_shift(modulation, rate)
        return np.clip(modulation, -1, 1)

    # Utility methods
    def allpass(self, data, length):
        allpass_filter = np.zeros(length)
        allpass_filter[0] = 1
        allpass_filter[-1] = -0.5
        allpass_output = np.convolve(data, allpass_filter, mode="same")
        allpass_output *= -0.5
        allpass_output[1:-1] +=
        allpass_output[:-1] += allpass_output[1:]
        return allpass_output, allpass_output[-1]

    def pitch_shift(self, data, shift_amount):
        output_data = np.zeros_like(data)
        if shift_amount >= 1:
            shift_amount = int(shift_amount)
            output_data[shift_amount:] = data[:-shift_amount]
        elif shift_amount <= -1:
            shift_amount = int(-shift_amount)
            output_data[:-shift_amount] = data[shift_amount:]
        else:
            return data
        return output_data

    # Processing method
    def process(self):
        # Check that input file is selected
        if not self.input_file_path:
            messagebox.showerror("Error", "No input file selected.")
            return

        # Load input file
        try:
            input_data, input_sample_rate = sf.read(self.input_file_path, dtype="float32")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load input file: {e}")
            return

        # Check that sample rate is supported
        if input_sample_rate not in SUPPORTED_SAMPLE_RATES:
            messagebox.showerror("Error", f"Input file has unsupported sample rate: {input_sample_rate}")
            return

        # Set input sample rate and output file path
        self.input_sample_rate = input_sample_rate
        if not self.output_file_path:
            self.output_file_path = os.path.splitext(self.input_file_path)[0] + "_processed.wav"

        # Apply effects
        if self.echo_checkbox_var.get():
            input_data = self.echo(input_data, self.echo_delay_var.get(), self.echo_decay_var.get())
        if self.reverb_checkbox_var.get():
            input_data = self.reverb(input_data, self.reverb_room_size_var.get(), self.reverb_decay_var.get())
        if self.chorus_checkbox_var.get():
            input_data = self.chorus(input_data, self.chorus_depth_var.get(), self.chorus_rate_var.get(), self.chorus_feedback_var.get())

        # Write output file
        try:
            sf.write(self.output_file_path, input_data, self.output_sample_rate)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save output file: {e}")
            return

        # Show message box
        messagebox.showinfo("Success", f"File processed and saved to: {self.output_file_path}")

    # Threading methods
    def play_thread_function(self):
        # Check that input file is selected
        if not self.input_file_path:
            messagebox.showerror("Error", "No input file selected.")
            return

        # Load input file
        try:
            input_data, input_sample_rate = sf.read(self.input_file_path, dtype="float32")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load input file: {e}")
            return

        # Check that sample rate is supported
        if input_sample_rate not in SUPPORTED_SAMPLE_RATES:
            messagebox.showerror("Error", f"Input file has unsupported sample rate: {input_sample_rate}")
            return

        # Apply effects
        if self.echo_checkbox_var.get():
            input_data = self.echo(input_data, self.echo_delay_var.get(), self.echo_decay_var.get())
        if self.reverb_checkbox_var.get():
            input_data = self.reverb(input_data, self.reverb_room_size_var.get(), self.reverb_decay_var.get())
        if self.chorus_checkbox_var.get():
            input_data = self.chorus(input_data, self.chorus_depth_var.get(), self.chorus_rate_var.get(), self.chorus_feedback_var.get())

       
def play(self):
    # Check that input file is selected
    if not self.input_file_path:
        messagebox.showerror("Error", "No input file selected.")
        return

    # Create audio player
    player = sa.play_buffer(b''.join(self.get_raw_data()), 2, 2, self.output_sample_rate)

    # Wait for player to finish
    player.wait_done()

def get_raw_data(self):
    # Load input file
    try:
        input_data, input_sample_rate = sf.read(self.input_file_path, dtype="float32")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load input file: {e}")
        return

    # Check that sample rate is supported
    if input_sample_rate not in SUPPORTED_SAMPLE_RATES:
        messagebox.showerror("Error", f"Input file has unsupported sample rate: {input_sample_rate}")
        return

    # Apply effects
    if self.echo_checkbox_var.get():
        input_data = self.echo(input_data, self.echo_delay_var.get(), self.echo_decay_var.get())
    if self.reverb_checkbox_var.get():
        input_data = self.reverb(input_data, self.reverb_room_size_var.get(), self.reverb_decay_var.get())
    if self.chorus_checkbox_var.get():
        input_data = self.chorus(input_data, self.chorus_depth_var.get(), self.chorus_rate_var.get(), self.chorus_feedback_var.get())

    # Pitch shift
    if self.pitch_shift_checkbox_var.get():
        shift_amount = self.pitch_shift_var.get()
        input_data = self.pitch_shift(input_data, shift_amount)

    # Resample
    if input_sample_rate != self.output_sample_rate:
        input_data = resampy.resample(input_data, input_sample_rate, self.output_sample_rate)

    # Convert to raw data
    raw_data = (input_data * 32767).astype(np.int16).tobytes()

    return raw_data
# File menu methods
def open_file_dialog(self):
    self.input_file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    self.input_file_label.config(text=f"Input file: {self.input_file_path}")

def save_file_dialog(self):
    self.output_file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
    self.output_file_label.config(text=f"Output file: {self.output_file_path}")

def exit_program(self):
    self.master.destroy()

# Help menu methods
def about_dialog(self):
    messagebox.showinfo("About", "Audio Processor v1.0\n\nCreated by John Smith")
Create GUI
root = Tk()
app = AudioProcessor(root)
root.mainloop()
