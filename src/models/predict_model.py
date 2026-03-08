import numpy as np  # noqa: F401
import pandas as pd
import joblib
import os

# ─── Paths ─────────────────────────────────────────────────────────────────────
MODELS_DIR = "models"

# ─── Feature Names (نفس ترتيب الـ preprocessing) ──────────────────────────────
DEFAULT_FEATURES = [
    "CreditScore", "Age", "Tenure", "Balance",
    "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary",
    "Gender_Male", "Geography_Germany", "Geography_Spain",
]


# ─── Load Scaler ───────────────────────────────────────────────────────────────
def load_scaler(path: str = None):
    """يحمّل الـ Scaler المحفوظ."""
    if path is None:
        path = os.path.join(MODELS_DIR, "scaler.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Scaler مش موجود: {path}")
    return joblib.load(path)


# ─── Load Model ────────────────────────────────────────────────────────────────
def load_model(model_name: str = "xgboost_model"):
    """يحمّل موديل محفوظ من الـ disk."""
    path = os.path.join(MODELS_DIR, f"{model_name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"الموديل مش موجود: {path}")
    return joblib.load(path)


# ─── Predict Single Customer ───────────────────────────────────────────────────
def predict_single(model, scaler, input_data: dict,
                   feature_names: list = None) -> dict:
    """
    يتنبأ لعميل واحد.

    Parameters:
        model        : الموديل المحمّل
        scaler       : الـ Scaler المحمّل
        input_data   : dict ببيانات العميل بعد الـ encoding
        feature_names: أسماء الـ features بالترتيب الصح

    Returns:
        dict: {prediction, label, churn_probability, risk_level}
    """
    if feature_names is None:
        feature_names = DEFAULT_FEATURES

    df        = pd.DataFrame([input_data])
    df        = df.reindex(columns=feature_names, fill_value=0)
    X_scaled  = scaler.transform(df)

    prediction  = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]
    prob_pct    = round(float(probability) * 100, 2)

    # ── Risk Level ──
    if prob_pct >= 70:
        risk = "HIGH"
    elif prob_pct >= 50:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    result = {
        "prediction":        int(prediction),
        "label":             "Churn" if prediction == 1 else "No Churn",
        "churn_probability": prob_pct,
        "risk_level":        risk,
    }

    print(f"النتيجة           : {'🔴 سيغادر' if prediction == 1 else '🟢 سيبقى'}")
    print(f"احتمالية المغادرة : {prob_pct}%")
    print(f"مستوى الخطر       : {risk}")
    return result


# ─── Predict Batch ─────────────────────────────────────────────────────────────
def predict_batch(model, scaler, df: pd.DataFrame,
                  feature_names: list = None) -> pd.DataFrame:
    """
    يتنبأ لمجموعة عملاء.

    Returns:
        DataFrame مع أعمدة: Prediction, Churn_Probability, Risk_Level
    """
    if feature_names is None:
        feature_names = DEFAULT_FEATURES

    df_input      = df.reindex(columns=feature_names, fill_value=0)
    X_scaled      = scaler.transform(df_input)
    predictions   = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)[:, 1]

    df = df.copy()
    df["Prediction"]        = predictions
    df["Churn_Probability"] = (probabilities * 100).round(2)
    df["Risk_Level"]        = df["Churn_Probability"].apply(
        lambda p: "HIGH" if p >= 70 else "MEDIUM" if p >= 50 else "LOW"
    )
    df["Label"] = df["Prediction"].map({0: "No Churn", 1: "Churn"})

    # ── Summary ──
    total   = len(df)
    churned = df["Prediction"].sum()
    print(f"\n📊 Batch Prediction Summary:")
    print(f"   Total    : {total:,}")
    print(f"   Churn    : {churned:,}  ({churned/total*100:.1f}%)")
    print(f"   No Churn : {total-churned:,}  ({(total-churned)/total*100:.1f}%)")

    return df


# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    model  = load_model("xgboost_model")
    scaler = load_scaler()

    # مثال عميل واحد
    sample = {
        "CreditScore":       600,
        "Age":               40,
        "Tenure":            5,
        "Balance":           50000.0,
        "NumOfProducts":     2,
        "HasCrCard":         1,
        "IsActiveMember":    1,
        "EstimatedSalary":   80000.0,
        "Gender_Male":       1,
        "Geography_Germany": 0,
        "Geography_Spain":   0,
    }

    print("─── Single Prediction ───")
    result = predict_single(model, scaler, sample)

    print("\n─── Batch Prediction ───")
    import pandas as pd
    batch_df = pd.DataFrame([sample, {**sample, "Age": 55, "IsActiveMember": 0, "Balance": 120000}])
    result_df = predict_batch(model, scaler, batch_df)
    print(result_df[["Prediction", "Churn_Probability", "Risk_Level", "Label"]])
