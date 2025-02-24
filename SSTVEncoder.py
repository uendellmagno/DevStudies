import numpy as np
import sounddevice as sd
import time
from tkinter import filedialog, Tk
from PIL import Image, UnidentifiedImageError
import pillow_heif
import os
from pysstv.color import (
    Robot36, PD120, MartinM1, MartinM2, ScottieS1, ScottieS2, ScottieDX
)

# OPTIONAL: Import alternative SSTV library for Robot 72 & Wraase SC2-180
try:
    from pystv import Robot72, WraaseSC2180
    ALT_SSTV_AVAILABLE = True
except ImportError:
    ALT_SSTV_AVAILABLE = False

# Constants
AUDIO_SAMPLE_RATE = 44100  # Standard audio sample rate
CHARACTER_TONE_DURATION = 0.1  # Duration of each character's sound
SILENCE_GAP_DURATION = 0.05  # Pause between character tones
DEFAULT_FREQUENCY = 440  # Default tone if character not mapped

# SSTV Encoding Modes
SSTV_MODES = {
    "1": ("Robot 36", Robot36),
    "2": ("PD 120", PD120),
    "3": ("Martin 1", MartinM1),
    "4": ("Martin 2", MartinM2),
    "5": ("Scottie 1", ScottieS1),
    "6": ("Scottie 2", ScottieS2),
    "7": ("Scottie DX", ScottieDX),
}

# Include extra modes if available
if ALT_SSTV_AVAILABLE:
    SSTV_MODES.update({
        "8": ("Robot 72", Robot72),
        "9": ("Wraase SC2-180", WraaseSC2180)
    })

# Character-to-Frequency Mapping
ASCII_FREQUENCIES = {chr(i): 300 + i * 10 for i in range(32, 127)}  # ASCII printable range

def convert_image_format(image_path):
    """Ensure the image is in a compatible format (e.g., convert HEIC to PNG)."""
    try:
        if image_path.lower().endswith(".heic"):
            heif_image = pillow_heif.open_heif(image_path)
            image = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
            converted_path = image_path.rsplit('.', 1)[0] + ".png"
            image.save(converted_path, format="PNG")
            return converted_path
        else:
            return image_path
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{image_path}'")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def generate_sine_wave(frequency, duration=CHARACTER_TONE_DURATION, sample_rate=AUDIO_SAMPLE_RATE):
    """Generate a sine wave for a given frequency and duration."""
    time_points = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * time_points)
    return (waveform * 32767).astype(np.int16)  # Convert to 16-bit PCM

def play_audio(audio_data, sample_rate=AUDIO_SAMPLE_RATE):
    """Play the generated audio."""
    sd.play(audio_data, sample_rate)
    sd.wait()

def text_to_tone_sequence(text):
    """Convert text to an audio sequence of tones representing each character."""
    combined_audio = np.array([], dtype=np.int16)
    silence = np.zeros(int(AUDIO_SAMPLE_RATE * SILENCE_GAP_DURATION), dtype=np.int16)

    for char in text:
        frequency = ASCII_FREQUENCIES.get(char, DEFAULT_FREQUENCY)
        tone = generate_sine_wave(frequency)
        combined_audio = np.concatenate((combined_audio, tone, silence))

    if combined_audio.size > 0:
        play_audio(combined_audio)
    else:
        print("No audio generated.")

def encode_image_to_sstv(image_path, mode_key):
    """Convert an image into an SSTV signal and play the generated sound."""
    if mode_key not in SSTV_MODES:
        print("Invalid SSTV mode selected.")
        return

    converted_path = convert_image_format(image_path)
    if not converted_path:
        return

    try:
        mode_name, sstv_class = SSTV_MODES[mode_key]
        image = Image.open(converted_path).convert("RGB").resize((320, 256))
        sstv_signal = sstv_class(image, AUDIO_SAMPLE_RATE, bits=8)
        audio_signal = np.array(list(sstv_signal.gen_samples()), dtype=np.float32)
        audio_signal /= np.max(np.abs(audio_signal))  # Normalize

        print(f"Playing SSTV {mode_name} signal...")
        sd.play(audio_signal, samplerate=AUDIO_SAMPLE_RATE)
        sd.wait()
        print(f"SSTV {mode_name} signal generated from {converted_path}")
    except Exception as error:
        print(f"Error encoding SSTV: {error}")

def select_image_and_encode_sstv():
    """Prompt user to select an image file and encode it into SSTV format."""
    try:
        root = Tk()
        root.withdraw()
        root.withdraw()
        root.update_idletasks()
        root.deiconify()
        root.lift()

        file_path = filedialog.askopenfilename()
        root.withdraw()

        if not file_path:
            print("No file selected.")
            return

        print("Choose SSTV mode:")
        for key, (name, _) in SSTV_MODES.items():
            print(f"{key}. {name}")

        mode_selection = input("Enter the number corresponding to your choice: ")
        encode_image_to_sstv(file_path, mode_selection)
    except Exception as error:
        print(f"Error with file dialog: {error}")

if __name__ == "__main__":
    # user_choice =
    print("Upload image for SSTV encoding:\n")

    # if user_choice == "1":
    #     text_input = input("Enter text: ")
    #     text_to_tone_sequence(text_input)
    # elif user_choice == "2":
    select_image_and_encode_sstv()
else:
    print("Invalid choice.")
