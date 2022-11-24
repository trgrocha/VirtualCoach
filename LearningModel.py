from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import recall_score, accuracy_score, confusion_matrix
from sklearn import metrics
import pandas as pd
import numpy as np
import datetime, time
import pickle 
import csv
import os

print ('Read landmarks')
df = pd.read_csv('landmarks.csv')

X = df.drop('class', axis=1) # features
y = df['class'] # target value

'''
pipelines = {
    'lr':make_pipeline(StandardScaler(), LogisticRegression()),
    'rc':make_pipeline(StandardScaler(), RidgeClassifier()),
    'rf':make_pipeline(StandardScaler(), RandomForestClassifier()),
    'gb':make_pipeline(StandardScaler(), GradientBoostingClassifier()),
}

fit_models = {}
for algo, pipeline in pipelines.items():
    model = pipeline.fit(X_train, y_train)
    fit_models[algo] = model

for algo, model in fit_models.items():
    yhat = model.predict(X_test)
    print(algo, accuracy_score(y_test, yhat))

'''
print ('Split data in Test and Train')

#Split data in Test and Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#Create Classifier
rfc = RandomForestClassifier(random_state=42, max_features='sqrt', n_estimators= 50, max_depth=4, criterion='gini')
#Train the model using the training sets 
rfc.fit(X_train, y_train)
y_pred=rfc.predict(X_test)

#metrics
print(accuracy_score(y_test,y_pred))
print(confusion_matrix(y_test,y_pred))

#print (RandomForestClassifier().get_params().keys())

print ('Saving Model')
with open('body_language.pkl', 'wb') as f:
    pickle.dump(rfc, f)

time.sleep(4) 

#input ("Modelo ...")
#exit()

#Retorna ao menu
exec(open("Menu.py").read())