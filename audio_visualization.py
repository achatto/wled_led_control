from requests import get, post
import json
from math import sqrt
import pyaudio
#import pygame
import numpy as np
import time
#import matplotlib.pyplot as plt
#import keyboard

def set_state(host, state):
    response = post(f"http://{host}/json/state", data=json.dumps(state))
    success = json.loads(response.text)
    return success["success"]

### Parameters

# Time params
dt = 0.1

#number of LED segments
n_seg = 8

# RGB INIT
g_channel = 0
b_channel = 1
r_channel = 2
col = np.zeros(3)

# Volume min max
min = 0.5
max = 75

### PyAudio INIT:

CHUNK = 2000 # Samples: 1024,  512, 256, 128
RATE = 40000  # Sampling rate

paud = pyaudio.PyAudio()

stream = paud.open(format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)

#SCREEN_HEIGHT = 100
#SCREEN_WIDTH = 100
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

### INIT LEDs
host = "192.168.178.124"

# define segments
seg = [0 for j in range(n_seg)]
for i in range(0,n_seg):
    seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'col': [[0, 0, 0, 0],[0,0,0,150],[0,0,0,0]], 'bri': 255}

#Set LED ON
for i in range(5):
    a = set_state(host, {"on": True})
    time.sleep(dt)
    if a == True:
        break
    elif i == 5:
        print("Error: Cannot turn LED on")
        exit

#set colors
data = {"seg": seg}
a = set_state(host, data)
if not a:
    print("Unsuccessful setting initial state /n")
time.sleep(dt)

# define black color
black = [[0, 0, 0, 0],[0,0,0,0],[0,0,0,0]]

done = False

while not done:
    # process events
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            done = True
#            break

    # Process audio data
    buffer = stream.read(CHUNK)
    waveform = np.frombuffer(buffer, dtype=np.int16)
    #print(np.mean(waveform**2))
    volume = sqrt(abs(np.mean(waveform**2)))
    volume = (np.clip(volume, min, max)-min)/(max-min)

    #map color values
    col[0] = volume
    col[2] = (1-volume)
    if volume >= 0.25 and volume <= 0.5:
        col[1] = (volume-0.25)/0.25
    elif volume > 0.5 and volume <= 0.75:
        col[1] = (volume-0.5)/0.25
    else:
        col[1] = 0
    col = col*255

    color =  [[col[0], col[1], col[2], 100],[0,0,0,0],[0,0,0,0]]
    #print(color)

    #map number of active led segments
    n_active_seg = int(volume//0.25)
    if n_active_seg == 4:
        n_active_seg = 3

 #   print(n_active_seg)
    for i in range(n_seg//2-n_active_seg-1, n_seg//2+n_active_seg+1): 
        seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'col': color, 'bri': 255}
    
    for i in range(0, n_seg//2-n_active_seg-1):
        seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'col': black, 'bri': 255}

    for i in range(n_seg//2+n_active_seg+1, n_seg):
        seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'col': black, 'bri': 255}
    
    data = {"seg": seg}
    a = set_state(host, data)
    if not a:
        print("Unsuccessful setting state /n")

    time.sleep(dt)
    # execute our drawing commands here
    #color = (0, 0, 200)



  #  for i in range(n_led // 2):
  
        #pygame.draw.line(screen, color, (0, SCREEN_HEIGHT//2 - i), (SCREEN_WIDTH,
        #   SCREEN_HEIGHT//2 - i))
        #pygame.draw.line(screen, color, (0, SCREEN_HEIGHT//2 + i), (SCREEN_WIDTH,
        #   SCREEN_HEIGHT//2 + i))
        

    #crop fft
    #fft = fft[50:CHUNK-51]
    
    #max_val = sqrt(max(v.real*v.real + v.imag*v.imag for v in fft))

    #scale_value = SCREEN_HEIGHT / max_val

    #for i,v in enumerate(fft):
    #    mag = sqrt(v.real*v.real + v.imag*v.imag)
    #    mapped_mag = mag*scale_value
    #    pygame.draw.line(screen, color, (i, SCREEN_HEIGHT//2), (i,
    #       SCREEN_HEIGHT - mapped_mag))

    # Flip the buffer
    #pygame.display.flip()
    #time.sleep(1)