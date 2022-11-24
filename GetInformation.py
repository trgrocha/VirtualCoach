import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import matplotlib.pyplot as plt
import datetime, time
import numpy as np
import pandas as pd
import csv
import os

class Graph:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.graph = np.zeros((height, width, 3), np.uint8)
    def update_frame(self, value):
        if value < 0:
            value = 0
        elif value >= self.height:
            value = self.height - 1
        new_graph = np.zeros((self.height, self.width, 3), np.uint8)
        new_graph[:,:-1,:] = self.graph[:,1:,:]
        new_graph[self.height - value:,-1,:] = 255
        self.graph = new_graph
    def get_graph(self):
        return self.graph

mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Try to obtain Video Index from the file
try:
    with open("video_index.txt", "r") as f:
      video_index_from_file = f.read()
except FileNotFoundError:
    video_index_from_file = 0 #Default Index   

# Open landmarks file
df = pd.read_csv('landmarks.csv')
unique_values = df['class'].unique()
unique_values_count = (len(unique_values))

if unique_values_count == 2:
    print("Pose: " + unique_values ) 
    print ('Two positions have already been reported.')
    print ('Please restart learning to enter new positions')
    time.sleep(5) # Sleep for 3 seconds
    exec(open("Menu.py").read())
else:
    print("Pose: " + unique_values ) 
    class_name = input("Enter the name of the exercise position (string):")
    varPose = input("Enter the number of captures of the pose (integer):")
    varTimer = int(varPose)

# Setup camera
cap = cv2.VideoCapture(int(video_index_from_file))
# Set a smaller resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
graph = Graph(100, 60)
prev_frame = np.zeros((480, 640), np.uint8)

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        image, frame = cap.read()
        frame.flags.writeable = False 
        #Moviment Graph  
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (25, 25), None)
        diff = cv2.absdiff(prev_frame, gray)
        difference = np.sum(diff)
        prev_frame = gray
        graph.update_frame(int(difference/42111))
        roi = frame[-70:-10, -110:-10,:]
        roi[:] = graph.get_graph()

        # Make Detections
        results = holistic.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # print(results.face_landmarks)
        
        # Recolor image back to BGR for rendering
        frame.flags.writeable = True   
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Pose Detections
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        # Export coordinates
        try:
            # Extract Pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
                          
            # Append class name 
            pose_row.insert(0, class_name)
            
            # Capture landmarks and Export to CSV
            with open('landmarks.csv', mode='a', newline='') as f:
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(pose_row) 

            # Get status box
            cv2.rectangle(frame, (0,0), (80, 60), (150, 110, 16), -1)
            
           # Display Probability
            cv2.putText(frame, 'INPUTS'
                        , (15,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, str(varTimer)
                        , (15,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
            
        except:
            pass
        # Display                
        cv2.imshow('Webcam', frame)

        #if varTimer == 50:
        #   input("Mudar")

        # Timer
        varTimer = varTimer - 1
        if cv2.waitKey(1) == 27 or varTimer < 0:
            break

cap.release()
cv2.destroyAllWindows()

#Retorna ao menu
exec(open("Menu.py").read())