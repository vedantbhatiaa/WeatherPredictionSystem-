from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from datetime import datetime, timedelta
import pytz
import requests

API_KEY = 'b54d670480a54316b87c8ade290fbfb5'
BASE_URL = 'https://api.weatherbit.io/v2.0/forecast/daily'    #Url for Daily Weather data.
API_KEY1 = '21276c37dacd7a3bce7bb37ba07855dd'
BASE_URL1 = 'https://api.openweathermap.org/data/2.5/'  #Url for Current Weather data.

## Fetch Current Weather Data.
def get_current_weather(city):
  url = f"{BASE_URL1}weather?q={city}&appid={API_KEY1}&units=metric"
  response = requests.get(url)
  data = response.json()
  return {
      "latitude": data["coord"]["lat"],
      "longitude": data["coord"]["lon"],
      "city": data["name"],
      "current_temp": round(data["main"]["temp"]), #celcius
      "feels_like": round(data["main"]["feels_like"]),#celcius
      "temp_min": round(data["main"]["temp_min"]),#celcius
      "temp_max": round(data["main"]["temp_max"]),#celcius
      "humidity": round(data["main"]["humidity"]),#percentage
      "wind_speed": data["wind"]["speed"],#m/s
      "description": data["weather"][0]["description"],
      "country": data["sys"]["country"],
      "clouds": data["clouds"]["all"],

  }


#1. Fetch Daily weather data (upto 30 days)
import requests
def get_daily_weather(city):
  url = f"{BASE_URL}daily?city={city}&key={API_KEY}&start_date=2025-03-24&end_date=2025-04-24&units=M"
  response = requests.get(url)
  data = response.json()
  return{
      "city_name": data["city_name"],
      "avg_temp": round(data["data"][0]["temp"]),     #celcius
      "min_temp": round(data["data"][0]["min_temp"]), #celcius
      "max_temp": round(data["data"][0]["max_temp"]), #celcius
      "humidity": round(data["data"][0]["rh"]),       #percentage
      "precipitation": data["data"][0]["precip"],     #mm
      "wind_speed": data["data"][0]["wind_spd"],      #m/s


  }

#2. Read Historical Data
def read_historical_data(filename):
  df = pd.read_csv(filename)
  df = df.dropna()
  df = df.drop_duplicates()
  return df

#3. Prepare data for training
def prepare_data(data):
  le = LabelEncoder()
  data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
  data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

  #define feature and target variables
  X = data[['MinTemp', 'MaxTemp', 'Humidity', 'Temp', 'WindSpeed']]
  y = data['RainTomorrow']

  return X, y, le

#4. Train Rain Prediction Model
def train_rain_model(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  MSE = mean_squared_error(y_test, y_pred)
  print(f"Accuracy: {accuracy}")
  print(f"Mean Squared Error: {MSE}")

  return model

#5. Prepare Regression Data(temperature, humidity, etc.)
def prepare_regression_data(data, feature):
  X, y = [], [] #initialize list for feature and target values

  for i in range(len(data) - 1):
    X.append(data[feature].iloc[i])
    y.append(data[feature].iloc[i + 1])

  X = np.array(X).reshape(-1, 1)
  y = np.array(y)

  return X, y

#6. Train Regression Model
def train_regression_model(X, y):
  model = RandomForestRegressor(n_estimators=100, random_state=0)
  model.fit(X, y)

  return model

#7. Predicting Future Values
def predict_future(model, current_value, days=15):
  predictions = [current_value]

  for i in range(days):
    next_value = model.predict(np.array([[predictions[-1]]]))
    predictions.append(next_value[0])

  return predictions[1:]

#8. Weather Analysis Function
def weather_view(request):
  context = {}

  if request.method =='POST':
    city = request.POST.get('city')
    daily_weather = get_daily_weather(city)
    current_weather = get_current_weather(city)

    #Loading historical data.
    csv_path = os.path.join('D:\\WeatherPrediction\\Dataset\\weather.csv')
    historical_data = read_historical_data(csv_path)

    #Prepare and train the rain prediction model.
    X, y, le = prepare_data(historical_data)

    rain_model = train_rain_model(X, y)

    daily_data = {

        'MinTemp': daily_weather['min_temp'],
        'MaxTemp': daily_weather['max_temp'],
        'Humidity': daily_weather['humidity'],
        'Temp': daily_weather['avg_temp'],
        'WindSpeed': daily_weather['wind_speed'],
    }

    daily_df = pd.DataFrame([daily_data])

    #Rain prediction.
    rain_prediction = rain_model.predict(daily_df)[0]

    #Preparing regression model for Temperature, Humidity and WindSpeed
    X_temp, y_temp = prepare_regression_data(historical_data, 'Temp')
    X_humidity, y_humidity = prepare_regression_data(historical_data, 'Humidity')
    X_windspeed, y_windspeed = prepare_regression_data(historical_data, 'WindSpeed')


    temp_model = train_regression_model(X_temp, y_temp)
    humidity_model = train_regression_model(X_humidity, y_humidity)
    windspeed_model = train_regression_model(X_windspeed, y_windspeed)

    #Predicting future Temperature and Humidity for next 5 days.
    future_temp = predict_future(temp_model, daily_weather['avg_temp'])
    future_humidity = predict_future(humidity_model, daily_weather['humidity'])
    future_windspeed = predict_future(windspeed_model, daily_weather['wind_speed'])


    #Preparing time for future predictions.
    timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(timezone)

    future_dates = [(current_time + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(15)]

    #Storing each day's predicted value seperately.
    day1, day2, day3, day4, day5, day6, day7, day8, day9, day10, day11, day12, day13, day14, day15 = future_dates
    temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10, temp11, temp12, temp13, temp14, temp15 = future_temp
    hum1, hum2, hum3, hum4, hum5, hum6, hum7, hum8, hum9, hum10, hum11, hum12, hum13, hum14, hum15 = future_humidity
    wind1, wind2, wind3, wind4, wind5, wind6, wind7, wind8, wind9, wind10, wind11, wind12, wind13, wind14, wind15 = future_windspeed

    #Pass data to a dictionary.
    context = {
      'location': city,
      'avg_temp': daily_weather['avg_temp'],
      'current_temp': current_weather['current_temp'],
      'feels_like': current_weather['feels_like'],
      'min_temp': daily_weather['min_temp'],
      'max_temp': daily_weather['max_temp'],
      'humidity': daily_weather['humidity'],
      'clouds': current_weather['clouds'],
      'description': current_weather['description'],
      'city': current_weather['city'],
      'country': current_weather['country'],

      'day1': day1,
      'day2': day2,
      'day3': day3,
      'day4': day4,
      'day5': day5,
      'day6': day6,
      'day7': day7,
      'day8': day8,
      'day9': day9,
      'day10': day10,
      'day11': day11,
      'day12': day12,
      'day13': day13,
      'day14': day14,
      'day15': day15,

      'temp1': f"{round(temp1, 1)}",
      'temp2': f"{round(temp2, 1)}",
      'temp3': f"{round(temp3, 1)}",
      'temp4': f"{round(temp4, 1)}",
      'temp5': f"{round(temp5, 1)}",
      'temp6': f"{round(temp6, 1)}",
      'temp7': f"{round(temp7, 1)}",
      'temp8': f"{round(temp8, 1)}",
      'temp9': f"{round(temp9, 1)}",
      'temp10': f"{round(temp10, 1)}",
      'temp11': f"{round(temp11, 1)}",
      'temp12': f"{round(temp12, 1)}",
      'temp13': f"{round(temp13, 1)}",
      'temp14': f"{round(temp14, 1)}",
      'temp15': f"{round(temp15, 1)}",

      'hum1': f"{round(hum1, 1)}",
      'hum2': f"{round(hum2, 1)}",
      'hum3': f"{round(hum3, 1)}",
      'hum4': f"{round(hum4, 1)}",
      'hum5': f"{round(hum5, 1)}",
      'hum6': f"{round(hum6, 1)}",
      'hum7': f"{round(hum7, 1)}",
      'hum8': f"{round(hum8, 1)}",
      'hum9': f"{round(hum9, 1)}",
      'hum10': f"{round(hum10, 1)}",
      'hum11': f"{round(hum11, 1)}",
      'hum12': f"{round(hum12, 1)}",
      'hum13': f"{round(hum13, 1)}",
      'hum14': f"{round(hum14, 1)}",
      'hum15': f"{round(hum15, 1)}",

      'wind1': wind1,
      'wind2': wind2,
      'wind3': wind3,
      'wind4': wind4,
      'wind5': wind5,
      'wind6': wind6,
      'wind7': wind7,
      'wind8': wind8,
      'wind9': wind9,
      'wind10': wind10,
      'wind11': wind11,
      'wind12': wind12,
      'wind13': wind13,
      'wind14': wind14,
      'wind15': wind15,

    }
    return render(request, 'weather.html', context)
  
  return render(request, 'weather.html', context)
