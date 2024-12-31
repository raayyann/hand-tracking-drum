# Hand Tracking Drum

This project uses a webcam and hand tracking to simulate playing a drum set. It uses OpenCV, MediaPipe, Pygame, and Mido for MIDI output.

## Requirements

- Python 3.9.x
- OpenCV
- MediaPipe
- Pygame
- Mido
- A webcam
- A MIDI output device (optional)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/raayyann/hand-tracking-drum.git
   cd hand-tracking-drum
   ```

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Ensure you have a MIDI output device configured if you want to use MIDI output.

## Usage

1. Run the script:

   ```sh
   python app.py
   ```

2. Use your webcam to play the virtual drums by moving your hands over the designated areas.

## MIDI Output

If `enable_midi_output` is set to `True`, the script will send MIDI messages to the configured MIDI output device.
