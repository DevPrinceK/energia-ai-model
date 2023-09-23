# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import pickle

# Load the dataset
# data = pd.read_csv("power_data.csv")
data = pd.read_csv("C:/Users/branana/Desktop/Github Repos/energia-ai-model/core/power_data.csv")

# Handle missing values (if any)
data.fillna(0, inplace=True) 

# Convert categorical variables to numerical using Label Encoding
label_encoders = {}
categorical_cols = ['Region', 'District', 'Town', 'Grid', 'Power_Outage']
# categorical_cols = ['Region', 'District', 'Town', 'Grid']
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le


print(data.head())
    
# save the label encoders if needed
with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day
data['DayOfWeek'] = data['Date'].dt.dayofweek

print(data.head())


# Train-Test Split
relevant_columns = ['Region', 'District', 'Town', 'Grid', 'Power_Consumption_MWh', 'Power_Generation_MWh', 'Year', 'Month', 'Day', 'DayOfWeek']
X = data[relevant_columns]
y = data['Power_Outage']
print( f"X-Head-AFTER: {X.head()}")
print(f"Y-head: {y.head()}")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Selection - Random Forest as an example
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Model Evaluation
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Model Deployment - Save the trained model if needed
pickle.dump(rf_model, open("rf_prediction_model.pkl", "wb"))

# Feature Importance
feature_importance = rf_model.feature_importances_
feature_names = X.columns
important_features = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance})
important_features = important_features.sort_values(by='Importance', ascending=False)
print("Feature Importance:")
print(important_features)

# Example using XGBoost
xgb_model = xgb.XGBClassifier(random_state=42)
xgb_model.fit(X_train, y_train)

# Further evaluation for XGBoost
y_pred_xgb = xgb_model.predict(X_test)
accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
print(f"XGBoost Accuracy: {accuracy_xgb:.2f}")

# Save the trained XGBoost model if needed
xgb_model.save_model("xgb_prediction_model.model")
