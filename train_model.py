import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Features + Label
X = df.drop("label", axis=1)
y = df["label"]

# Train Random Forest
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("✅ Random Forest Model Trained Successfully")