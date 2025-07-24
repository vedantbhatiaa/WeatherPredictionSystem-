# Weather Prediction and Agriculture Impact 🚜🌦️

This project analyzes and predicts weather patterns to assess their impact on agriculture using advanced machine learning models (ARIMA and LSTM). By utilizing weather data from Mumbai (2010–2021), we aim to provide actionable forecasts to help farmers make informed decisions.




## 📊 Project Overview
Agriculture is highly sensitive to unpredictable weather. This project focuses on predicting key weather parameters—precipitation, temperature, humidity, and rainfall—to improve agricultural planning and resilience. We used ARIMA for linear trends and LSTM for capturing complex, nonlinear patterns.




## 📁 Dataset
- **Sources:**  
  - Kaggle: Historical weather data (2016–2021)  
  - Provided by Guide: Extended dataset (2010–2021)  
- **Parameters:** Precipitation, Temperature, Humidity, Rainfall  
- **Location:** Mumbai, India  



## 🛠️ Methodology
1. **Data Collection:** Combined datasets from Kaggle and guide-provided sources.
2. **Data Cleaning & Preprocessing:** Handled null values, removed duplicates, standardized units using Python libraries.
3. **Feature Selection:** Selected five significant parameters through statistical methods.
4. **Data Analysis:** Performed extensive analysis using pandas and SQL for data querying.
5. **Visualization:** Created insightful plots with matplotlib to understand trends and relationships.
6. **Modeling:**  
   - **ARIMA:** Captured linear patterns in time series data.
   - **RANDOM FOREST:** Captured pattern for shorter intervals
   - **LSTM:** Modeled complex, nonlinear patterns for better predictions.  
7. **Evaluation:** Assessed model performance using R² and RMSE under a univariate setup.



## 📈 Results
- **LSTM** outperformed ARIMA with lower MSE and RMSE values.
- **Prediction Accuracy:** LSTM and Random Forest provided superior results for complex weather patterns.
- **Impact:** Accurate forecasts can help farmers plan crops, irrigation, and mitigate risks.



## 🖥️ Technologies Used
- Python 🐍  
- Jupyter Notebook 📓  
- SQL 🗄️  
- Libraries: pandas, numpy, matplotlib, seaborn, statsmodels, tensorflow/keras  



## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-agriculture-impact.git

2. Clone the repository:
   ```bash
   pip install -r requirements.txt
   
3. Run the Jupiter Notebook:
  ```bash
  jupyter notebook Weather_Prediction.ipynb

