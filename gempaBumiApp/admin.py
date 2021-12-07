from typing import final
from django.contrib import admin
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from datetime import datetime
import pandas as pd 
import numpy as np
from gempaBumiApp.models import Gempa, Prediksi_Gempa

# Register your models here.
admin.site.register(Gempa)
admin.site.register(Prediksi_Gempa)

if Gempa.objects.all().count() == 0:
    
    df = pd.read_csv(r"E:\Python\Django\MachineLearningGempaBumiIndonesia\DATA\database.csv")

# Priview Data CSV
# print(df.head())
    for index, row in df.iterrows():
        Lat = row['Lat']
        Lon = row['Lon']
        Depth = row['Depth']
        Mag = row['Mag']
        Region = row['Region']
        Date = row['Date']

        Gempa(Lat=Lat, Lon=Lon, Depth=Depth, Mag=Mag, Region=Region, Date=Date).save()

if Prediksi_Gempa.objects.all().count() == 0:
    # menambahkan data 2021 dan data dari 2017 - 2020 yang sudah di test
    df_test = pd.read_csv(r"E:\Python\Django\MachineLearningGempaBumiIndonesia\DATA\Gempa2021.csv")
    df_train = pd.read_csv(r"E:\Python\Django\MachineLearningGempaBumiIndonesia\DATA\database.csv")
    
    # olah data data frame data test
    df_test['dateInt']=df_test['Year'].astype(str) + df_test['Month'].astype(str).str.zfill(2)+ df_test['Day'].astype(str).str.zfill(2)
    df_test['Date']= pd.to_datetime(df_test['dateInt'], format='%Y%m%d')
    
    # Membersihkan dataframe
    df_test_load = df_test[['Date','Lat','Lon','Mag','Depth']]
    df_train = df_train[['Date','Lat','Lon','Mag','Depth']]
    
    # Remove null Safety
    df_train.dropna()
    df_test_load.dropna()
    
    # Melatih data
    X = df_train[['Lat','Lon']]
    y = df_train[['Mag','Depth']]
    
    X_new = df_test_load[['Lat','Lon']]
    y_new = df_test_load[['Mag','Depth']]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model
    # Create random forest regressor model
    model_reg = RandomForestRegressor(random_state=50)
    # Train the model using the training data
    model_reg.fit(X_train, y_train)
    # Use the trained model to predict the training test data
    model_reg.predict(X_test)
    
    # Improve the model accuracy by automating hyperparameter tuning
    parameters = {'n_estimators': [10, 20, 50, 100, 200, 500]}
    # Create the gridsearchcv model
    grid_obj = GridSearchCV(model_reg, parameters)
    # Train the model using the training data
    grid_fit = grid_obj.fit(X_train, y_train)
    # Select the best fit model
    best_fit = grid_fit.best_estimator_
    # Use the best fit model to make the prediction on our training test data
    results = best_fit.predict(X_test)
    # Preview score
    score = best_fit.score(X_test, y_test) * 100
    
    # Use the best fit model to make the prediction on our out of sample test data (quakes for year 2017)
    final_results = best_fit.predict(X_new)
    # Evaluate the model accuracy
    final_score = best_fit.score(X_new, y_new) * 100
    
    lst_Magnitudes = []
    lst_Depth = []
    i = 0

    # Loop through our predicted magnitude and depth values and then store them in our lists
    for r in final_results.tolist():
        lst_Magnitudes.append(final_results[i][0])
        lst_Depth.append(final_results[i][1])
        i += 1

    df_results = X_new[['Lat','Lon']]
    df_results['Mag'] = lst_Magnitudes
    df_results['Depth'] = lst_Depth
    df_results['Score'] = final_score
    
    for index, row in df_results.iterrows():
        Lat = row['Lat']
        Lon = row['Lon']
        Mag = row['Mag']
        Depth = row['Depth']
        Score = row['Score']
        
        Prediksi_Gempa(Lat=Lat, Lon=Lon, Mag=Mag, Depth=Depth, Score=Score).save()
    # print(score)