import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "phishing.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "phishing_model.pkl"
)


# ==========================================
# 13 FEATURES
# ==========================================

feature_columns = [
    "url_length",
    "valid_url",
    "at_symbol",
    "sensitive_words_count",
    "path_length",
    "isHttps",
    "nb_dots",
    "nb_hyphens",
    "nb_and",
    "nb_or",
    "nb_www",
    "nb_com",
    "nb_underscore"
]


# ==========================================
# LOAD DATASET
# ==========================================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)

print("Dataset columns:")
print(df.columns.tolist())


# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

required_columns = feature_columns + ["target"]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# ==========================================
# CREATE X AND Y
# ==========================================

X = df[feature_columns]

y = df["target"]


# ==========================================
# CLEAN DATA
# ==========================================

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

y = pd.to_numeric(
    y,
    errors="coerce"
)


# Remove invalid rows

valid_rows = X.notna().all(axis=1) & y.notna()

X = X[valid_rows]

y = y[valid_rows]


# ==========================================
# DISPLAY INFORMATION
# ==========================================

print("\nTraining features:")
print(X.columns.tolist())

print("\nTraining data shape:")
print(X.shape)

print("\nTarget distribution:")
print(y.value_counts())


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# TRAIN RANDOM FOREST
# ==========================================

print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(
    X_train,
    y_train
)


# ==========================================
# TEST MODEL
# ==========================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n========================================")
print("MODEL TRAINING COMPLETED")
print("========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)


print("\nModel saved successfully:")
print(MODEL_PATH)

print("\n========================================")