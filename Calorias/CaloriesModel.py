# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split , GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle
import csv

# %matplotlib inline
from matplotlib import style
style.use("seaborn")

from IPython.display import HTML
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

calories = pd.read_csv('calories.csv')
exercise = pd.read_csv('exercise.csv')
df_exercise = exercise.merge(calories , on = "User_ID")

# Remover a coluna de controle User_ID
df_exercise.drop(columns = "User_ID" , inplace = True)

df_exercise.to_csv('atividades.csv', index=False)

exercise_train_data , exercise_test_data = train_test_split(df_exercise , test_size = 0.3 , random_state = 1)

# Criação do grupo classificatório el relação a idade
age_groups = ["Young" , "Middle-Aged" , "Old"]
exercise_train_data["age_groups"] = pd.cut(exercise_train_data["Age"] , bins = [20 , 40 ,60 , 80] , right = False , labels = age_groups)
exercise_train_data["age_groups"].head()
exercise_train_data["age_groups"].value_counts()

# Criação da coluna de BMI = IMC
#A fórmula do IMC (Índice de Massa Corporal) - IMC = Peso / Altura ^2
for data in [exercise_train_data , exercise_test_data]:        
  data["BMI"] = data["Weight"] / ((data["Height"] / 100) ** 2)
  data["BMI"] = round(data["BMI"] , 2)

# Classificação de acordo com o IMC
bmi_category = ["Very severely underweight" , "Severely underweight" , "Underweight" , "Normal" ,
                "Pre-obesity" , "Obese Class I" , "Obese Class II" , "Obese Class III"]

exercise_train_data["Categorized_BMI"] = pd.cut(exercise_train_data["BMI"] , bins = [0 , 15 , 16 , 18.5 , 25 , 30 , 35 , 40 , 50]
                                              , right = False , labels = bmi_category)

exercise_train_data["Categorized_BMI"] = exercise_train_data["Categorized_BMI"].astype("object") # converting 'categorical'

#Calculo da frequência cardíaca máxima
exercise_train_data['FCM'] = 220 - exercise_train_data['Age']
exercise_test_data['FCM'] = 220 - exercise_train_data['Age']

# Classificação da Zona de FC de acordo com a idade e a FCM
def define_zone(HR, FCM):
  x = round(HR/FCM,1)   
  if (x > 0.9 ):
    return 'Maximum'
  elif (x > 0.8 and x <= 0.9):
    return 'Hard'
  elif (x > 0.7 and x <= 0.8):
    return 'Moderate'
  elif (x > 0.6 and x <= 0.7):
    return 'Light'
  else:
    return 'Very Light'
  #ref https://www.polar.com/br/smart-coaching/what-are-heart-rate-zones

# Criação da Zone de FC
exercise_train_data['Heart_Rate_Zone'] = exercise_train_data[['Heart_Rate', 'FCM']].apply(lambda x: define_zone(x[0],x[1]), axis=1)

"""# **Construção do Modelo**"""

#Antes de alimentarmos nossos dados para o modelo, temos que primeiro converter a coluna categórica (como Gênero) em coluna numérica.
exercise_train_data = exercise_train_data[["Gender" , "Age" , "BMI" , "Duration" , "Heart_Rate" , "Calories"]]
exercise_test_data = exercise_test_data[["Gender" , "Age" , "BMI"  , "Duration" , "Heart_Rate" , "Calories"]]
exercise_train_data = pd.get_dummies(exercise_train_data, drop_first = True)
exercise_test_data = pd.get_dummies(exercise_test_data, drop_first = True)

#Separar X e y para o conjunto de treinamento e o conjunto de teste.
X_train = exercise_train_data.drop("Calories" , axis = 1)
y_train = exercise_train_data["Calories"]

X_test = exercise_test_data.drop("Calories" , axis = 1)
y_test = exercise_test_data["Calories"]

#Building Regression Model
linreg = LinearRegression()
linreg.fit(X_train , y_train)
linreg_prediction = linreg.predict(X_test)

#Avaliação do Modelo - Regression Model
print("Linear Regression Mean Absolute Error(MAE) : " , round(metrics.mean_absolute_error(y_test , linreg_prediction) , 2))
print("Linear Regression Mean Squared Error(MSE) : " , round(metrics.mean_squared_error(y_test , linreg_prediction) , 2))
print("Linear Regression Root Mean Squared Error(RMSE) : " , round(np.sqrt(metrics.mean_squared_error(y_test , linreg_prediction)) , 2))

#Building RandomForestRegressor
random_reg = RandomForestRegressor(n_estimators = 1000 , max_features = 3 , max_depth = 6)
random_reg.fit(X_train , y_train)
random_reg_prediction = random_reg.predict(X_test)

# Avaliação do Modelo - RandomForestRegressor
print("RandomForest Mean Absolute Error(MAE) : " , round(metrics.mean_absolute_error(y_test , random_reg_prediction) , 2))
print("RandomForest Mean Squared Error(MSE) : " , round(metrics.mean_squared_error(y_test , random_reg_prediction) , 2))
print("RandomForest Root Mean Squared Error(RMSE) : " , round(np.sqrt(metrics.mean_squared_error(y_test , random_reg_prediction)) , 2))

exercise_train_data.iloc[50]

# Age, BMI=IMC, Duration, Heart Rate, Genero (0 = Male and 1 = Femmale)
X_array = np.array([[38 ,19.14 , 5 , 90 , 0]]).reshape(1 , -1)

y_pred = random_reg.predict(X_array)
print("RF Prediction : " , round(y_pred[0] , 2))

y_pred = linreg.predict(X_array)
print("LG Prediction : " , round(y_pred[0] , 2))

#Gravação do modelo linreg_prediction
with open('linreg_prediction.pkl', 'wb') as f:
    pickle.dump(linreg, f)

#Gravação do modelo random_reg_prediction
with open('random_reg_prediction.pkl', 'wb') as f:
    pickle.dump(random_reg, f)