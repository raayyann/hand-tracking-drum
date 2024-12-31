import cv2
import mediapipe as mp
import pygame
import mido
import time

pygame.mixer.init()

kick_drum = pygame.mixer.Sound('sounds/kick_drum.wav')
snare_drum = pygame.mixer.Sound('sounds/snare_drum.wav')
hihat_drum = pygame.mixer.Sound('sounds/hihat_drum.wav')
crash_drum = pygame.mixer.Sound('sounds/crash_drum.wav')
open_hihat_drum = pygame.mixer.Sound('sounds/open_hihat_drum.wav')

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

drum_areas = {
    "kick": (250, 150, 550, 450),
    "snare": (650, 150, 950, 450),
    "hihat": (1050, 150, 1350, 450),
    "crash": (1450, 150, 1750, 450),
    "open_hihat": (1450, 500, 1750, 800),
}

midi_notes = {
    "kick": 36,
    "snare": 38,
    "hihat": 42,
    "crash": 49,
    "open_hihat": 46,
}

# For midi output
enable_midi_output = False

if enable_midi_output:
    midi_out = mido.open_output("IAC Driver Bus 1") # Change this to your MIDI output

last_played = {
    "kick": 0,
    "snare": 0,
    "hihat": 0,
    "crash": 0,
    "open_hihat": 0,
}

cooldown_time = 0.2

def play_drum_sound(area):
    current_time = time.time()
    if current_time - last_played[area] < cooldown_time:
        return
    last_played[area] = current_time

    if not enable_midi_output:
        if area == "kick":
            kick_drum.play()
        elif area == "snare":
            snare_drum.play()
        elif area == "hihat":
            hihat_drum.play()
            open_hihat_drum.stop()
        elif area == "crash":
            crash_drum.play()
        elif area == "open_hihat":
            open_hihat_drum.play()
            hihat_drum.stop()

    if enable_midi_output and area in midi_notes:
        note = midi_notes[area]
        midi_out.send(mido.Message('note_on', note=note, velocity=100))
        midi_out.send(mido.Message('note_off', note=note, velocity=0))

hands_touched_drum = {}

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    for drum, (x1, y1, x2, y2) in drum_areas.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, drum, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    for hand_index in hands_touched_drum:
        hands_touched_drum[hand_index]["detected"] = False

    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            index_finger_tip = hand_landmarks.landmark[8]
            x, y = int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0])

            if hand_index not in hands_touched_drum:
                hands_touched_drum[hand_index] = {"drum": None, "detected": True}
            else:
                hands_touched_drum[hand_index]["detected"] = True

            for drum, (x1, y1, x2, y2) in drum_areas.items():
                if x1 < x < x2 and y1 < y < y2:
                    if hands_touched_drum[hand_index]["drum"] != drum:
                        play_drum_sound(drum)
                        hands_touched_drum[hand_index]["drum"] = drum
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    break
            else:
                hands_touched_drum[hand_index]["drum"] = None

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    hands_touched_drum = {k: v for k, v in hands_touched_drum.items() if v["detected"]}

    cv2.imshow("main drum pake kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if enable_midi_output:
    midi_out.close()