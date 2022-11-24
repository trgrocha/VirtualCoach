import mediapipe as mp
import cv2
import pandas as pd
import numpy as np
import datetime, time
import pickle 
import csv
import os
import warnings
warnings.filterwarnings('ignore')

print ('Start Process')
Person = input("Enter your name (string): ")
Age = input("Enter your age (integer): ")
Gender = input("Enter your gender (F) Female (M) Male: ")
#ExerciseNr = int(input("Enter the exercise (0) The last one (1)Squat  (2)Lunge-R (3)Lunge-L: "))
Repetitions = int(input("Enter the number of repetitions (integer): "))
print ('Read Model')
"""
if ExerciseNr == 1:
    with open('Squat.pkl', 'rb') as f:
        model = pickle.load(f)
    ExerciseName = 'Squat'
    PoseOne = 'upstanding'
    PoseTwo = 'squat'
elif ExerciseNr == 2:
    with open('LungeR.pkl', 'rb') as f:
        model = pickle.load(f)
    ExerciseName = 'LungeR'
    PoseOne = 'upstanding'
    PoseTwo = 'forward'
elif ExerciseNr == 3:
    with open('LungeL.pkl', 'rb') as f:
        model = pickle.load(f)
    ExerciseName = 'LungeL'
    PoseOne = 'upstanding'
    PoseTwo = 'forward'
else: 
"""
with open('body_language.pkl', 'rb') as f:
    model = pickle.load(f)
df = pd.read_csv('landmarks.csv')
unique_values = df['class'].unique()
ExerciseName = 'Other'
PoseOne = unique_values[0]
PoseTwo = unique_values[1]

print ('Set Variables')
mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions    
Quantity = 0
Control = 0
Acurracity = 0.70
QualityExecution = []
Position = []

# Try to obtain Video Index from the file
try:
    with open("video_index.txt", "r") as f:
        video_index_from_file = f.read()
except FileNotFoundError:
    video_index_from_file = 0 #Default Index 

cap = cv2.VideoCapture(int(video_index_from_file))
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False        
        results = holistic.process(image)
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        # Export coordinates
        try:
            # Extract Pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                        
            # Make Detections
            X = pd.DataFrame([pose_row])
            body_language_class = model.predict(X)[0]
            body_language_prob = model.predict_proba(X)[0]
            #print(body_language_class, body_language_prob)
            
            # coords
            coords = tuple(np.multiply(
                            np.array(
                                (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE].x, 
                                 results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE].y))
                        , [640,480]).astype(int))

            ANKLE = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x

            # Get status box
            cv2.rectangle(image, (0,0), (640, 60), (150, 110, 16), -1)
            
            # Display Class
            cv2.putText(image, 'MOVIMENT', (150,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, body_language_class.split(' ')[0], (130,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
         
            # Display Probability
            cv2.putText(image, 'PROBABILITY', (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2)), (25,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

            # Display Feedback
            AcurracityNow = body_language_prob[np.argmax(body_language_prob)]
            cv2.putText(image, 'FEEDBACK', (400,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            if body_language_class.split(' ')[0] == PoseTwo and Control == 1:
               Control = 0
               Position.append(PoseTwo)
               QualityExecution.append(AcurracityNow)

            elif body_language_class.split(' ')[0] == PoseOne and Control == 0:          
               Control = 1
               Quantity += 1
               Position.append(PoseOne)
               QualityExecution.append(AcurracityNow)
               dfAnalysis = pd.DataFrame({'precision':QualityExecution,'position':Position, 'person':Person, 
                                           'age':Age, 'gender':Gender, 'exercise': ExerciseName, 
                                           'target':Acurracity})        
               


            if body_language_prob[np.argmax(body_language_prob)] > Acurracity:
               cv2.putText(image, 'GOOD', (300,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 0), 2, cv2.LINE_AA)
            else:
               cv2.putText(image, 'BAD', (300,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2, cv2.LINE_AA)

            # Display Counter
            cv2.putText(image, 'COUNTER', (550,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(Quantity), (570,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            
        except:
            pass
        cv2.imshow('Test Learning', image)

        if cv2.waitKey(1) == 27:
            break
        elif Quantity >= Repetitions: 
            dfAnalysis.to_csv('exercise.csv', mode='a', index=False, header=False)
            break

cap.release()
cv2.destroyAllWindows()
#Call Menu
exec(open("Menu.py").read())