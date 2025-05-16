from math import sqrt
import pyaudio
import pygame
import numpy as np
import time

# PyAudio INIT:
CHUNK = 1024 # Samples: 1024,  512, 256, 128
RATE = 20000  # Equivalent to Human Hearing at 40 kHz
INTERVAL = 1  # Sampling Interval in Seconds ie Interval to listen

paud = pyaudio.PyAudio()

stream = paud.open(format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)

SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((CHUNK, SCREEN_HEIGHT))

done = False
while not done:
    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

    # Process data
    buffer = stream.read(CHUNK)
    waveform = np.frombuffer(buffer, dtype=np.int16)
    volume = sum(waveform)/CHUNK

    fft = np.fft.fft(waveform)

    # Clear screen to black
    screen.fill((0, 0, 0))

    # execute our drawing commands here
    color = (0, 0, 200)

    #crop fft
    fft = fft[50:CHUNK-51]
    
    max_val = sqrt(max(v.real*v.real + v.imag*v.imag for v in fft))

    scale_value = SCREEN_HEIGHT / max_val

    for i,v in enumerate(fft):
        mag = sqrt(v.real*v.real + v.imag*v.imag)
        mapped_mag = mag*scale_value
        pygame.draw.line(screen, color, (i, SCREEN_HEIGHT), (i,
           SCREEN_HEIGHT - mapped_mag))

    # Flip the buffer
    pygame.display.flip()
    #time.sleep(0.1)