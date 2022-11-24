import csv
import os
import time

print ('The pose data will be erased, do you want to continue?')
varStatus = input("Inform (S) to Confirm or (N) to Cancel: ")

if varStatus == 's' or varStatus == 'S':
    landmarks = ['class','x1','y1','z1','v1','x2','y2','z2','v2','x3','y3','z3','v3','x4','y4','z4','v4','x5','y5','z5','v5','x6','y6','z6','v6','x7','y7','z7','v7','x8','y8','z8','v8','x9','y9','z9','v9','x10','y10','z10','v10','x11','y11','z11','v11','x12','y12','z12','v12','x13','y13','z13','v13','x14','y14','z14','v14','x15','y15','z15','v15','x16','y16','z16','v16','x17','y17','z17','v17','x18','y18','z18','v18','x19','y19','z19','v19','x20','y20','z20','v20','x21','y21','z21','v21','x22','y22','z22','v22','x23','y23','z23','v23','x24','y24','z24','v24','x25','y25','z25','v25','x26','y26','z26','v26','x27','y27','z27','v27','x28','y28','z28','v28','x29','y29','z29','v29','x30','y30','z30','v30','x31','y31','z31','v31','x32','y32','z32','v32','x33','y33','z33','v33']
    with open('landmarks.csv', mode='w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(landmarks)
    #Call Menu
    print ('Data erased')
    time.sleep(2) # Sleep for 3 seconds
    exec(open("Menu.py").read())
else:
    exec(open("Menu.py").read())
    