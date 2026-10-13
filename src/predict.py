
import pandas as pd
import joblib
from pathlib import Path
from src.feature_extraction import extract_features

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "phishing_model.pkl"

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

model = joblib.load(MODEL_PATH)


def predict_with_confidence(url):
    url = url.strip()

    if not url:
        raise ValueError("Please enter a website URL.")

    features = extract_features(url)

    if len(features) != len(feature_columns):
        raise ValueError(
            f"Expected {len(feature_columns)} features, "
            f"but got {len(features)}"
        )

    input_data = pd.DataFrame(
        [features],
        columns=feature_columns
    )

    prediction = model.predict(input_data)[0]

    if prediction == 0:
        result = "PHISHING WEBSITE"
    elif prediction == 1:
        result = "LEGITIMATE WEBSITE"
    else:
        result = "UNKNOWN"

    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0]
        confidence = float(max(probabilities) * 100)

    return result, confidence


def predict_website(url):
    result, confidence = predict_with_confidence(url)
    return result


if __name__ == "__main__":
    url = input("Enter website URL: ").strip()

    try:
        result, confidence = predict_with_confidence(url)

        print("\n================================")
        print("URL:", url)
        print("Prediction:", result)

        if confidence is not None:
            print(f"Confidence: {confidence:.2f}%")

        print("================================")

    except Exception as error:
        print("Prediction error:", error)
