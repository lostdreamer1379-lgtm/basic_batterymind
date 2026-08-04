import joblib

features = joblib.load("models/feature_columns.pkl")

print("Number of features:", len(features))
print(features)