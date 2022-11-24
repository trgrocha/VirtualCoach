
from bluepy.btle import BTLEDisconnectError
from cursesmenu import *
from cursesmenu.items import *
from matplotlib import pyplot as plt
from miband import miband
import keyboard  # using module keyboard
import numpy as np
import pandas as pd
import argparse
import subprocess
import time
from datetime import datetime
import csv
import sys
import os

#Duration = input("Enter the duration time in seconds: ")

#-------------- Set variables
Age = input("Enter your age (integer): ")
Gender = input("Enter your gender (F) Female (M) Male: ")
Weight = input("Enter your Weight: ")

MHR = 220 - int(Age)
HR90 = round(int(MHR * 0.90))
HR80 = round(int(MHR * 0.80))
HR70 = round(int(MHR * 0.70))
HR60 = round(int(MHR * 0.60))
HR50 = round(int(MHR * 0.50))
HeartRateAvarage = 0
HeartRate = []
Tempo = []
#RHR = 55
#VO2max = 15.3 * (MHR / RHR)

#------- GRAPH -------------
plt.close() 
fig=plt.figure()
#fig, ax = plt.subplots()

#------- DATA ABOUT USER ---
def endmonitor():
    os.system('clear') #Linux 
    print ("Age: " + str(Age))
    print ("Gender: " + str(Gender))
    print ("Weight: " + str(Weight))
    print ("--------------------------- Heart Rate Zones -------------------- ")
    print ("MHR = Maximum Heart Rate: " + str(MHR))
    print ("VO2 Max Zone   - Maximum     90% - 100% : " + str(HR90) + " - " + str(MHR))
    print ("Anaerobic Zone - Hard        80% - 90%  : " + str(HR80) + " - " + str(HR90))
    print ("Aerobic Zone   - Moderate    70% - 80%  : " + str(HR70) + " - " + str(HR80))
    print ("Fat Burn Zone  - Light       60% - 70%  : " + str(HR60) + " - " + str(HR70))
    print ("Warm Up Zone   - Very  Light 50% - 60%  : " + str(HR50) + " - " + str(HR60))
    print ("-------------- Calories Burned Based on Heart Rate  ------------- ")
    #df = pd.read_csv('heart.csv')
    #df.head(10)
    input ("Monitoring finished press to continue ...")
    exit()

#--------- MIBAND INICIALIZATION -------------
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mac', required=False, help='Set mac address of the device')
parser.add_argument('-k', '--authkey', required=False, help='Set Auth Key for the device')
args = parser.parse_args()

# Try to obtain MAC from the file
try:
    with open("mac.txt", "r") as f:
        mac_from_file = f.read().strip()
except FileNotFoundError:
    mac_from_file = None

# Use appropriate MAC
if args.mac:
    MAC_ADDR = args.mac
elif mac_from_file:
    MAC_ADDR = mac_from_file
else:
    print("Error:")
    print("  Please specify MAC address of the MiBand")
    print("  Pass the --mac option with MAC address or put your MAC to 'mac.txt' file")
    print("  Example of the MAC: a1:c2:3d:4e:f5:6a")
    exit(1)

# Validate MAC address
if 1 < len(MAC_ADDR) != 17:
    print("Error:")
    print("  Your MAC length is not 17, please check the format")
    print("  Example of the MAC: a1:c2:3d:4e:f5:6a")
    exit(1)

# Try to obtain Auth Key from file
try:
    with open("auth_key.txt", "r") as f:
        auth_key_from_file = f.read().strip()
except FileNotFoundError:
    auth_key_from_file = None

# Use appropriate Auth Key
if args.authkey:
    AUTH_KEY = args.authkey
elif auth_key_from_file:
    AUTH_KEY = auth_key_from_file
else:
    print("Warning:")
    print("  To use additional features of this script please put your Auth Key to 'auth_key.txt' or pass the --authkey option with your Auth Key")
    print()
    AUTH_KEY = None
    
# Validate Auth Key
if AUTH_KEY:
    if 1 < len(AUTH_KEY) != 32:
        print("Error:")
        print("  Your AUTH KEY length is not 32, please check the format")
        print("  Example of the Auth Key: 8fa9b42078627a654d22beff985655db")
        exit(1)

# Convert Auth Key from hex to byte format
if AUTH_KEY:
    AUTH_KEY = bytes.fromhex(AUTH_KEY)

# ------------ MIBAND FEATURES ------------
# Needs Auth
def general_info():
    print ('MiBand')
    print ('Soft revision:',band.get_revision())
    print ('Hardware revision:',band.get_hrdw_revision())
    print ('Serial:',band.get_serial())
    print ('Battery:', band.get_battery_info()['level'])
    print ('Time:', band.get_current_time()['date'].isoformat())
    input('Press a key to continue')

# Needs Auth
def heart_logger(data):
    HeartRate.append(data)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    Tempo.append(current_time)
    dfAnalise = pd.DataFrame({'BPM':data,'Tempo':Tempo})
    plt.clf()                  
    plt.plot(HeartRate,'k')
    plt.ylabel('Heart Rate')
    plt.xlabel('Time')
    plt.title('Heart Rate Training Zone')
    plt.axhspan(50, HR50, facecolor='lightblue', alpha=1)
    plt.axhspan(HR50, HR70, facecolor='lime', alpha=1)
    plt.axhspan(HR70, HR80, facecolor='yellow', alpha=1)
    plt.axhspan(HR80, HR90, facecolor='orange', alpha=1)
    plt.axhspan(HR90, MHR, facecolor='tomato', alpha=1)
    plt.ylim([50, MHR]) 
    plt.ioff() #interactive mode on
    plt.pause(0.001)
    if keyboard.is_pressed("q"):
        dfAnalise.to_csv('heart.csv')
        endmonitor()

# Needs Auth
def get_realtime():
    band.start_heart_rate_realtime(heart_measure_callback=heart_logger)

if __name__ == "__main__":
    success = False
    while not success:
        try:
            if (AUTH_KEY):
                band = miband(MAC_ADDR, AUTH_KEY, debug=True)
                success = band.initialize()
                get_realtime()
            else:
                band = miband(MAC_ADDR, debug=True)
                success = True
            break
        except BTLEDisconnectError:
            print('Connection to the MIBand failed. Trying out again in 3 seconds')
            time.sleep(3)
            continue
        except KeyboardInterrupt:
            print("\nExit.")
            exit()