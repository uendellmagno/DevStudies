#!/usr/bin/env python3
"""
Refactored SSTV Transmitter with Real-Time Control.
"""

import os
import tempfile
import threading
from tkinter import filedialog, Tk

import numpy as np
import sounddevice as sd
from PIL import Image, ImageOps, ImageDraw, ImageFont
import pillow_heif
from pysstv.color import (
    MartinM1, MartinM2, ScottieS1, ScottieS2, ScottieDX, Robot36,
    PasokonP3, PasokonP5, PasokonP7, PD90, PD120, PD160, PD180, PD240, PD290,
    WraaseSC2120, WraaseSC2180
)

################################################################################
# Constants
################################################################################

AUDIO_SAMPLE_RATE = 44100
CHARACTER_TONE_DURATION = 0.1
SILENCE_GAP_DURATION = 0.05
DEFAULT_FREQUENCY = 440

END_TONE_DURATION = 5.0

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
# Interrupt Controller
################################################################################

class InterruptController:
    """
    A simple controller to handle user interrupts via a threading.Event.
    """

    def __init__(self) -> None:
        self.event = threading.Event()

    def reset(self) -> None:
        self.event.clear()

    def set(self) -> None:
        self.event.set()

    def is_set(self) -> bool:
        return self.event.is_set()


interrupt_controller = InterruptController()
global_lock = threading.Lock()  # For any shared resource protection


################################################################################
# Helper Functions
################################################################################

def convert_image_format(image_path: str) -> str:
    """
    Convert a HEIC image to PNG if needed.
    """
    try:
        if image_path.lower().endswith(".heic"):
            heif_image = pillow_heif.open_heif(image_path)
            image = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
            converted_path = os.path.splitext(image_path)[0] + ".png"
            image.save(converted_path, format="PNG")
            return converted_path
        return image_path
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def prepare_image(image: Image.Image, target_size: tuple, callsign: str = None) -> Image.Image:
    """
    Resize an image to the target size and overlay a callsign if provided.
    """
    try:
        image = ImageOps.fit(image, target_size, method=Image.LANCZOS)
    except Exception:
        image = image.resize(target_size, Image.LANCZOS)

    if callsign:
        try:
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except Exception:
                font = ImageFont.load_default(20)
            draw.text((10, 10), callsign, fill="white", font=font,
                      stroke_width=3, stroke_fill="black")
        except Exception as e:
            print(f"Error adding callsign: {e}")
    return image


################################################################################
# Audio Generation Functions
################################################################################

def generate_sine_wave(freq: float, duration: float) -> np.ndarray:
    """
    Generate a sine wave for a given frequency and duration.
    """
    t = np.linspace(0, duration, int(AUDIO_SAMPLE_RATE * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)


def generate_handshake_prefix(duration: float = 1.5) -> np.ndarray:
    """
    Generate the handshake prefix signal.
    """
    segments = [
        np.linspace(1800, 2600, int(AUDIO_SAMPLE_RATE * 0.3)),
        np.linspace(2200, 1200, int(AUDIO_SAMPLE_RATE * 0.3)),
        np.full(int(AUDIO_SAMPLE_RATE * 0.2), 2100),
        np.random.uniform(1000, 3000, int(AUDIO_SAMPLE_RATE * 0.4)),
        np.linspace(1800, 800, int(AUDIO_SAMPLE_RATE * 0.3)),
    ]
    wave_parts = [generate_sine_wave(f, len(f) / AUDIO_SAMPLE_RATE) for f in segments]
    prefix_wave = np.concatenate(wave_parts)[:int(AUDIO_SAMPLE_RATE * duration)]
    prefix_wave = prefix_wave / np.max(np.abs(prefix_wave))
    return prefix_wave.astype(np.float32)


def generate_end_tone_wave(mode_key: str) -> np.ndarray:
    """
    Generate an end tone wave based on the SSTV mode.
    """
    frequency = SSTV_END_TONES.get(mode_key, 1500.0)
    t = np.linspace(0, END_TONE_DURATION, int(AUDIO_SAMPLE_RATE * END_TONE_DURATION))
    modulation = 0.25 * np.sin(2 * np.pi * 0.5 * t)
    wave = 0.5 * (1 + modulation) * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32)


################################################################################
# Audio Control Functions
################################################################################

def wait_for_interrupt() -> None:
    """
    Wait for the user to press 'f' (followed by Enter) to trigger an interrupt.
    """
    while True:
        user_input = input().strip().lower()
        if user_input == 'f':
            with global_lock:
                interrupt_controller.set()
            break


def play_interruptible(audio_data: np.ndarray, mode_key: str = None) -> None:
    """
    Play audio data with real-time interrupt control.
    """
    data = audio_data.copy()

    def callback(outdata, frames, time, status):
        nonlocal data
        if status:
            print(status)

        if len(data) == 0:
            raise sd.CallbackStop

        chunksize = min(frames, len(data))
        outdata[:chunksize, 0] = data[:chunksize]
        data = data[chunksize:]

        if interrupt_controller.is_set():
            raise sd.CallbackStop

    with global_lock:
        interrupt_controller.reset()

    stream = sd.OutputStream(
        samplerate=AUDIO_SAMPLE_RATE,
        blocksize=1024,
        channels=1,
        callback=callback,
        dtype='float32'
    )

    # Start a thread to listen for an interrupt.
    input_thread = threading.Thread(target=wait_for_interrupt, daemon=True)
    input_thread.start()

    with stream:
        while stream.active:
            sd.sleep(100)

    # If playback was interrupted and a mode_key was provided, play the end tone.
    if interrupt_controller.is_set() and mode_key:
        end_tone = generate_end_tone_wave(mode_key)
        sd.play(end_tone, AUDIO_SAMPLE_RATE)
        sd.wait()


################################################################################
# Core Functionality
################################################################################

def encode_image_to_sstv(image_path: str, mode_key: str, callsign: str = None) -> None:
    """
    Encode an image into an SSTV signal and transmit it.
    """
    if mode_key not in SSTV_MODES:
        print("Invalid SSTV mode")
        return

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
        full_signal = full_signal / np.max(np.abs(full_signal))

        print(f"Transmitting {mode_name} - Press 'f' + Enter to cancel")
        play_interruptible(full_signal, mode_key)

    except Exception as e:
        print(f"Error: {e}")


def generate_modem_handshake() -> None:
    """
    Generate and transmit a modem handshake signal.
    """
    handshake = np.array([], dtype=np.float32)

    # Dial tone
    t = np.linspace(0, 2, 2 * AUDIO_SAMPLE_RATE, endpoint=False)
    dial_tone = 0.3 * (np.sin(2 * np.pi * 350 * t) + np.sin(2 * np.pi * 440 * t))
    handshake = np.concatenate((handshake, dial_tone))

    # DTMF tones
    dtmf_tones = [(941, 1336), (852, 1209), (770, 1477), (697, 1633)]
    for low, high in dtmf_tones:
        t = np.linspace(0, 0.07, int(0.07 * AUDIO_SAMPLE_RATE), endpoint=False)
        tone = 0.3 * (np.sin(2 * np.pi * low * t) + np.sin(2 * np.pi * high * t))
        silence = np.zeros(int(0.04 * AUDIO_SAMPLE_RATE))
        handshake = np.concatenate((handshake, tone, silence))

    handshake = handshake / np.max(np.abs(handshake))
    handshake = handshake.astype(np.float32)
    print("Playing modem handshake - Press 'f' + Enter to cancel")
    play_interruptible(handshake)


def generate_text_image(target_size, text, padding=20):
    """
    Generate an image with text that automatically wraps and scales to fit the target size.
    """
    target_width, target_height = target_size
    image = Image.new('RGB', target_size, (0, 0, 0))  # Black background
    draw = ImageDraw.Draw(image)

    if not text.strip():
        return image

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    font_size = 40
    min_font_size = 12
    line_spacing = 1.1
    max_line_width = target_width - 2 * padding
    vertical_padding = padding // 2

    while font_size >= min_font_size:
        try:
            font = font.font_variant(size=font_size)
        except AttributeError:
            pass

        lines = []
        for paragraph in text.split('\n'):
            words = paragraph.split()
            current_line = []
            current_length = 0

            for word in words:
                word_length = font.getlength(word + ' ')
                if current_length + word_length <= max_line_width:
                    current_line.append(word)
                    current_length += word_length
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = word_length
                    else:
                        lines.append(word)

            if current_line:
                lines.append(' '.join(current_line))

        total_text_height = len(lines) * font_size * line_spacing

        if total_text_height + 2 * vertical_padding <= target_height:
            break

        font_size -= 2

    y = (target_height - total_text_height) // 2
    for line in lines:
        text_width = font.getlength(line)
        x = (target_width - text_width) // 2
        draw.text((x, y), line, fill="white", font=font)
        y += int(font_size * line_spacing)

    return image


################################################################################
# User Interface
################################################################################

def select_image_and_encode_sstv() -> None:
    """
    Main user interface loop to select transmission options.
    """
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

            # Get callsign (or text) input.
            callsign = input("Enter callsign/text to send: ").strip()

            print("\nChoose transmission type:")
            print("1. Text only (send callsign as image)")
            print("2. Image file (add callsign overlay)")
            input_type = input("Select (1/2): ").strip()

            if input_type == '1':
                mode_name, sstv_class, target_size = SSTV_MODES[choice]
                image = generate_text_image(target_size, callsign)
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
                    temp_path = tmpfile.name
                    image.save(temp_path, 'PNG')
                encode_image_to_sstv(temp_path, choice)
                os.remove(temp_path)

            elif input_type == '2':
                root = Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename()
                if not file_path:
                    continue
                encode_image_to_sstv(file_path, choice, callsign or None)
            else:
                print("Invalid transmission type selected")

        except Exception as e:
            print(f"Error: {e}")


################################################################################
# Main
################################################################################

def main() -> None:
    """
    Main entry point.
    """
    select_image_and_encode_sstv()


if __name__ == "__main__":
    main()
