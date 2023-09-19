from sklearn.metrics import mean_squared_error
import pickle
import pandas as pd
import numpy as np
from sklearn.calibration import LabelEncoder
import pmdarima as pm
#fit the model
from statsmodels.tsa.vector_ar.var_model import VAR


# Load the dataset
# data = pd.read_csv("power_data.csv")
data = pd.read_csv(
    "C:/Users/branana/Desktop/Github Repos/energia-ai-model/core/power_data.csv")

# Handle missing values (if any)
data.fillna(0, inplace=True)

# Convert categorical variables to numerical using Label Encoding
label_encoders = {}
categorical_cols = ['Region', 'District', 'Town', 'Grid']
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le


# save the label encoders if needed
with open("forecast_label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])
# data['Year'] = data['Date'].dt.year
# data['Month'] = data['Date'].dt.month
# data['Day'] = data['Date'].dt.day
# data['DayOfWeek'] = data['Date'].dt.dayofweek


# Set DateTime as the index
data.set_index('Date', inplace=True)

# Split the data into training and testing sets
train_size = int(len(data) * 0.8)
train_data, test_data = data[:train_size], data[train_size:]

# Fit Auto SARIMA model for multiple targets
# targets = ['Power_Consumption_MWh', 'Power_Generation_MWh']
# models = {}
# for target in targets:
#     model = pm.auto_arima(train_data[target], exogenous=train_data[[
#                           'Region', 'District', 'Town', 'Grid', 'Year', 'Month', 'Day', 'DayOfWeek' ]], seasonal=True, m=30)
#     models[target] = model
for i in [1,2,3,4,5,6,7,8,9,10]:
    model = VAR(endog=train_data[[
                           'Region', 'District', 'Town', 'Grid', 'Power_Consumption_MWh', 'Power_Generation_MWh' ]])
    model_fit = model.fit(i)
    print('Order =', i)
    print('AIC: ', model_fit.aic)
    print('BIC: ', model_fit.bic)
    print()
    
result = model.fit(5)
print(result.summary())    



lagged_Values = train_data[[
                           'Region', 'District', 'Town', 'Grid','Power_Consumption_MWh', 'Power_Generation_MWh' ]].values[-8:]
pred = result.forecast(y=lagged_Values, steps=12) 

idx = pd.date_range('2018-12-31', periods=12, freq='D')
df_forecast=pd.DataFrame(data=pred, index=idx, columns=['Region', 'District', 'Town', 'Grid','Power_Consumption_MWh', 'Power_Generation_MWh'])

print(df_forecast)
print(train_data[['Region', 'District', 'Town', 'Grid','Power_Consumption_MWh', 'Power_Generation_MWh']])
#print(pred)
# make prediction on validation
# prediction = model_fit.forecast( steps=2)
# print(prediction)
# for model in models:
#     with open(f"forecast_{model}.pkl", "wb") as f:
#         pickle.dump(model, f)

# Forecast for each target
# forecasts = {}
# for target in targets:
#     forecast, conf_int = models[target].predict(n_periods=len(test_data), exogenous=test_data[[
#                                                 'Region', 'District', 'Town', 'Grid', 'Year', 'Month', 'Day', 'DayOfWeek' ]], return_conf_int=True)
#     forecasts[target] = forecast


# Print the forecasts for each target
# for target in targets:
#     print(f"Forecasted {target}:")
#     print(forecasts[target])


# Evaluate the model, e.g., using RMSE or other relevant metrics
# errors = {}
# for target in targets:
#     rmse = np.sqrt(mean_squared_error(test_data[target], forecast))
#     print("\nRoot Mean Squared Error (RMSE):", rmse)
