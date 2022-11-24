from pickletools import int4
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import datetime, time
import pickle
import csv
import os
import warnings
warnings.filterwarnings('ignore')

#Load models 
print ("Load Model")
#with open('random_reg_prediction.pkl', 'rb') as f:
#   random_reg = pickle.load(f)
with open('D:\Code\TCC\linreg_prediction.pkl', 'rb') as f:
   linreg = pickle.load(f)

os.system('cls') #Linux 
#Set Param
Age = int(input("Enter your age (integer): "))
Gender = int(input("Enter your gender (1) Female (0) Male: "))
Weight = float(input("Enter your Weight i.e 77.5: "))
Height = float(input("Enter your Height i.e 1.77: "))
HeartRateAvarage = int(input("Enter Mean Heart Rate : "))
Duration = int(input("Enter the duration in minutes : "))

MHR = 220 - int(Age)
HR90 = round(int(MHR * 0.90))
HR80 = round(int(MHR * 0.80))
HR70 = round(int(MHR * 0.70))
HR60 = round(int(MHR * 0.60))
HR50 = round(int(MHR * 0.50))
BMI = Weight / ((Height) ** 2)

if Gender == 0:
  dsGender = 'Male'
else:
  dsGender = 'Female'

os.system('cls') #Linux 
print ("--------------------------- Information  -------------------- ")
print ("Age: " + str(Age))
print ("Gender: " + dsGender)
print ("Weight: " + str(Weight))
print ("Height: " + str(Height))
print ("BMI: " + str(round(BMI,2)))
print ("Hear Rate: " + str(HeartRateAvarage))
print ("Duration: " + str(Duration))
print ("")
print ("--------------------------- Heart Rate Zones -------------------- ")
print ("MHR = Maximum Heart Rate: " + str(MHR))
print ("VO2 Max Zone   - Maximum     90% - 100% : " + str(HR90) + " - " + str(MHR))
print ("Anaerobic Zone - Hard        80% - 90%  : " + str(HR80) + " - " + str(HR90))
print ("Aerobic Zone   - Moderate    70% - 80%  : " + str(HR70) + " - " + str(HR80))
print ("Fat Burn Zone  - Light       60% - 70%  : " + str(HR60) + " - " + str(HR70))
print ("Warm Up Zone   - Very  Light 50% - 60%  : " + str(HR50) + " - " + str(HR60))
print("")
print ("-------------- Prediction of Calories Burned Based on Heart Rate ------------- ")
# Age, BMI=IMC, Duration, Heart Rate, Genero (0 = Male and 1 = Femmale)
X_array = np.array([[Age, BMI , Duration , HeartRateAvarage , Gender]]).reshape(1 , -1)
y_pred = linreg.predict(X_array)
print("Calories : " , round(y_pred[0] , 2))
print("")
input("Press enter to continue")

#Retorna ao menu
exec(open("Menu.py").read())