import numpy as np
import pandas as pd
import joblib
import os


def load_scaler(path: str = "models/scaler.pkl"):
    """يحمّل الـ Scaler المحفوظ."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Scaler مش موجود: {path}")
    return joblib.load(path)


def predict_single(model, scaler, input_data: dict, feature_names: list) -> dict:
    """
    يتنبأ لعميل واحد.

    Parameters:
        model: الموديل المحمّل
        scaler: الـ Scaler المحمّل
        input_data (dict): بيانات العميل
        feature_names (list): أسماء الـ Features بالترتيب الصح

    Returns:
        dict: النتيجة (prediction + probability)
    """
    df = pd.DataFrame([input_data])

    # تأكد إن الـ columns بالترتيب الصح
    df = df.reindex(columns=feature_names, fill_value=0)

    # Scale
    X_scaled = scaler.transform(df)

    # Predict
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]

    result = {
        "prediction": int(prediction),
        "label": "🔴 سيغادر (Churn)" if prediction == 1 else "🟢 سيبقى (No Churn)",
        "churn_probability": round(float(probability) * 100, 2)
    }

    print(f"النتيجة: {result['label']}")
    print(f"احتمالية المغادرة: {result['churn_probability']}%")

    return result


def predict_batch(model, scaler, df: pd.DataFrame, feature_names: list) -> pd.DataFrame:
    """
    يتنبأ لمجموعة عملاء.

    Returns:
        DataFrame مع عمودين: Prediction و Churn_Probability
    """
    df_input = df.reindex(columns=feature_names, fill_value=0)
    X_scaled = scaler.transform(df_input)

    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]

    df['Prediction'] = predictions
    df['Churn_Probability'] = (probabilities * 100).round(2)

    return df


if __name__ == "__main__":
    # مثال بسيط
    from src.models.train_model import load_model

    model = load_model("xgboost_model")
    scaler = load_scaler()

    # بيانات عميل تجريبية (بعد encoding)
    sample = {
        'CreditScore': 600,
        'Age': 40,
        'Tenure': 5,
        'Balance': 50000,
        'NumOfProducts': 2,
        'HasCrCard': 1,
        'IsActiveMember': 1,
        'EstimatedSalary': 80000,
        'Gender_Male': 1,
        'Geography_Germany': 0,
        'Geography_Spain': 0
    }

    feature_names = list(sample.keys())
    result = predict_single(model, scaler, sample, feature_names)
