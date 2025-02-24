import numpy as np
import sounddevice as sd
from tkinter import filedialog, Tk
from PIL import Image, UnidentifiedImageError, ImageOps, ImageDraw, ImageFont
import pillow_heif
import os
import threading
from pysstv.color import (
    MartinM1, MartinM2, ScottieS1, ScottieS2, ScottieDX, Robot36,
    PasokonP3, PasokonP5, PasokonP7, PD90, PD120, PD160, PD180, PD240, PD290,
    WraaseSC2120, WraaseSC2180
)

# Global control variables
global_interrupt = False
global_lock = threading.Lock()

################################################################################
# Constants
################################################################################
AUDIO_SAMPLE_RATE = 44100
CHARACTER_TONE_DURATION = 0.1
SILENCE_GAP_DURATION = 0.05
DEFAULT_FREQUENCY = 440

END_TONE_DURATION = 15.0  # 15-second end tone
SSTV_END_TONES = {
    "1": 1200.0, "2": 1200.0, "3": 1200.0, "4": 1200.0, "5": 1200.0,
    "6": 1900.0, "7": 1900.0, "8": 1900.0, "9": 1900.0, "10": 2300.0,
    "11": 2300.0, "12": 2300.0, "13": 2300.0, "14": 2300.0, "15": 2300.0,
    "16": 1500.0, "17": 1500.0,
}

SSTV_MODES = {
    "1": ("Martin M1", MartinM1, (320, 256)),
    "2": ("Martin M2", MartinM2, (320, 256)),
    "3": ("Scottie S1", ScottieS1, (320, 256)),
    "4": ("Scottie S2", ScottieS2, (320, 256)),
    "5": ("Scottie DX", ScottieDX, (320, 256)),
    "6": ("Robot 36", Robot36, (320, 256)),
    "7": ("Pasokon P3", PasokonP3, (320, 256)),
    "8": ("Pasokon P5", PasokonP5, (320, 256)),
    "9": ("Pasokon P7", PasokonP7, (320, 256)),
    "10": ("PD 90", PD90, (320, 256)),
    "11": ("PD 120", PD120, (320, 256)),
    "12": ("PD 160", PD160, (320, 256)),
    "13": ("PD 180", PD180, (320, 256)),
    "14": ("PD 240", PD240, (320, 256)),
    "15": ("PD 290", PD290, (320, 256)),
    "16": ("Wraase SC 2120", WraaseSC2120, (320, 256)),
    "17": ("Wraase SC 2180", WraaseSC2180, (320, 256)),
}


################################################################################
# Helper functions
################################################################################
def convert_image_format(image_path):
    try:
        if image_path.lower().endswith(".heic"):
            heif_image = pillow_heif.open_heif(image_path)
            image = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
            converted_path = image_path.rsplit('.', 1)[0] + ".png"
            image.save(converted_path, format="PNG")
            return converted_path
        return image_path
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def prepare_image(image, target_size, callsign=None):
    try:
        image = ImageOps.fit(image, target_size, method=Image.LANCZOS)
    except:
        image = image.resize(target_size, Image.LANCZOS)

    if callsign:
        try:
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            draw.text((10, 10), callsign, fill="white", font=font,
                      stroke_width=2, stroke_fill="black")
        except Exception as e:
            print(f"Error adding callsign: {e}")
    return image


################################################################################
# Audio Generation
################################################################################
def generate_sine_wave(freq, duration):
    t = np.linspace(0, duration, int(AUDIO_SAMPLE_RATE * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


def generate_handshake_prefix(duration=1.5):
    segments = [
        np.linspace(1800, 2600, int(AUDIO_SAMPLE_RATE * 0.3)),
        np.linspace(2200, 1200, int(AUDIO_SAMPLE_RATE * 0.3)),
        np.full(int(AUDIO_SAMPLE_RATE * 0.2), 2100),
        np.random.uniform(1000, 3000, int(AUDIO_SAMPLE_RATE * 0.4)),
        np.linspace(1800, 800, int(AUDIO_SAMPLE_RATE * 0.3)),
    ]
    wave_parts = [generate_sine_wave(f, len(f) / AUDIO_SAMPLE_RATE) for f in segments]
    prefix_wave = np.concatenate(wave_parts)[:int(AUDIO_SAMPLE_RATE * duration)]
    return (prefix_wave / np.max(np.abs(prefix_wave))).astype(np.float32)


def generate_end_tone_wave(mode_key):
    frequency = SSTV_END_TONES.get(mode_key, 1500.0)
    t = np.linspace(0, END_TONE_DURATION, int(AUDIO_SAMPLE_RATE * END_TONE_DURATION))
    modulation = 0.25 * np.sin(2 * np.pi * 0.5 * t)
    wave = 0.5 * (1 + modulation) * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32)


################################################################################
# Audio Control
################################################################################
def play_interruptible(audio_data, mode_key=None):
    global global_interrupt
    audio_data = audio_data.copy()

    def callback(outdata, frames, time, status):
        nonlocal audio_data
        if status:
            print(status)

        available = len(audio_data)
        if available == 0:
            raise sd.CallbackStop

        chunksize = min(frames, available)
        outdata[:chunksize] = audio_data[:chunksize].reshape(-1, 1)
        audio_data = audio_data[chunksize:]

        if global_interrupt:
            raise sd.CallbackStop

    with global_lock:
        global_interrupt = False

    stream = sd.OutputStream(
        samplerate=AUDIO_SAMPLE_RATE,
        blocksize=1024,
        channels=1,
        callback=callback,
        dtype='float32'
    )

    input_thread = threading.Thread(target=wait_for_interrupt)
    input_thread.start()

    with stream:
        while stream.active:
            sd.sleep(100)

    if global_interrupt and mode_key:
        end_tone = generate_end_tone_wave(mode_key)
        sd.play(end_tone, AUDIO_SAMPLE_RATE)
        sd.wait()


def wait_for_interrupt():
    global global_interrupt
    while True:
        user_input = input().strip().lower()
        if user_input == 'f':
            with global_lock:
                global_interrupt = True
            break


################################################################################
# Core Functionality
################################################################################
def encode_image_to_sstv(image_path, mode_key, callsign=None):
    converted_path = convert_image_format(image_path)
    if not converted_path:
        return

    try:
        mode_name, sstv_class, target_size = SSTV_MODES[mode_key]
        with Image.open(converted_path) as img:
            image = prepare_image(img.convert("RGB"), target_size, callsign)

        sstv_signal = sstv_class(image, AUDIO_SAMPLE_RATE, bits=8)
        sstv_wave = np.array(list(sstv_signal.gen_samples()), dtype=np.float32)

        prefix_wave = generate_handshake_prefix()
        full_signal = np.concatenate([prefix_wave, sstv_wave])
        full_signal /= np.max(np.abs(full_signal))

        print(f"Transmitting {mode_name} - Press 'f' + Enter to cancel")
        play_interruptible(full_signal, mode_key)

    except Exception as e:
        print(f"Error: {str(e)}")


def generate_modem_handshake():
    handshake = np.array([], dtype=np.float32)

    # Dial tone
    t = np.linspace(0, 2, 2 * AUDIO_SAMPLE_RATE)
    dial_tone = 0.3 * (np.sin(2 * np.pi * 350 * t) + np.sin(2 * np.pi * 440 * t))
    handshake = np.concatenate((handshake, dial_tone))

    # DTMF tones
    dtmf = [(941, 1336), (852, 1209), (770, 1477), (697, 1633)]
    for low, high in dtmf:
        t = np.linspace(0, 0.07, int(0.07 * AUDIO_SAMPLE_RATE))
        tone = 0.3 * (np.sin(2 * np.pi * low * t) + np.sin(2 * np.pi * high * t))
        handshake = np.concatenate((handshake, tone, np.zeros(int(0.04 * AUDIO_SAMPLE_RATE))))

    # Normalize and play
    handshake = (handshake / np.max(np.abs(handshake))).astype(np.float32)
    print("Playing modem handshake - Press 'f' + Enter to cancel")
    play_interruptible(handshake)


################################################################################
# User Interface
################################################################################
def select_image_and_encode_sstv():
    while True:
        try:
            print("\n" + "=" * 40)
            print("SSTV Transmitter with Real-Time Control")
            print("=" * 40)
            for key, (name, _, _) in SSTV_MODES.items():
                print(f"{key.rjust(2)}: {name}")
            print("HK: Dial-up Handshake")
            print(" Q: Quit")

            choice = input("Select option: ").strip().upper()
            if choice == "Q":
                break
            if choice == "HK":
                generate_modem_handshake()
                continue
            if choice not in SSTV_MODES:
                print("Invalid selection")
                continue

            root = Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            if not file_path:
                continue

            callsign = input("Optional callsign (press Enter to skip): ").strip()
            encode_image_to_sstv(file_path, choice, callsign or None)

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    select_image_and_encode_sstv()