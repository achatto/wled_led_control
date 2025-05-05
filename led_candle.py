from requests import get, post
import json
import time
import numpy as np

def set_state(host, state):
    response = post(f"http://{host}/json/state", data=json.dumps(state))
    success = json.loads(response.text)
    return success["success"]

host = "192.168.178.124"

phase = np.arange(0, 2*np.pi, 2*np.pi/8)
#phase = [0 for i in range(8)]
#np.random.shuffle(phase)
freq = 1
min_amp = 0.10
r = [255, 255, 200, 200, 200, 200, 200, 200]
g = [50, 100, 100, 100, 100, 100, 100, 50]
b = [0, 0, 0, 0, 0, 00, 150, 150]

ww = [100, 150, 150, 150, 150, 150, 150, 200]

# define segments
seg_start_stop = [[0 for i in range(2)] for j in range(int(60/8+1))]
seg = [0 for j in range(int(60/8+1))]
for i in range(0,int(60/8)+1):
    seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'col': [[r[i], g[i], b[i], ww[i]],[0,0,0,0],[0,0,0,0]]}

## Set LED ON
for i in range(5):
    a = set_state(host, {"on": True})
    time.sleep(0.1)
    if a == True:
        break
    elif i == 5:
        print("Error: Cannot turn LED on")
        exit
#set colors
data = {"seg": seg}
#print(data)
a = set_state(host, data)
if not a:
    print("Unsuccessful setting initial state /n")
time.sleep(0.1)

#start = time.monotonic()
counter = 0
while 1:
    counter = (counter + 1)%100000 
    t = 0.1*counter
#    t = time.monotonic()-start
    for i in range(0,int(60/8)+1):
        bri = int(255*(min_amp+(1-min_amp)*(1+np.sin(2*np.pi*t*freq+phase[i]))/2))
        #print(((1-min_amp)*(1+np.sin(2*np.pi*t*freq+phase[i]))/2))
        print(bri)
        #bri = 100
        seg[i] = {'id': i, 'start': i*8, 'stop': int(np.clip((i+1)*8, 0, 60)), 'bri': bri}
    data = {"seg": seg}
    a = set_state(host, data)
    if not a:
        print("Unsuccessful setting state /n")
    time.sleep(0.1)



    

    

    
    