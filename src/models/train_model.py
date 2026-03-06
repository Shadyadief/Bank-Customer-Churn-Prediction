import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression


MODELS_DIR = "models"

# إعدادات الموديلات بناءً على الـ Tuning اللي عملناه
MODELS = {
    "logistic_regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),
    "random_forest": RandomForestClassifier(
        random_state=42
    ),
    "xgboost_model": XGBClassifier(
        learning_rate=0.2,
        max_depth=7,
        n_estimators=300,
        subsample=0.8,
        random_state=42,
        eval_metric='logloss'
    )
}


def train_model(model, X_train, y_train, model_name: str, models_dir: str = "models"):
    """
    يدرّب موديل واحد ويحفظه.

    Parameters:
        model: الموديل
        X_train: بيانات التدريب
        y_train: الـ Labels
        model_name: اسم الموديل للحفظ

    Returns:
        الموديل بعد التدريب
    """
    print(f"🚀 بيدرّب: {model_name}...")
    model.fit(X_train, y_train)

    os.makedirs(models_dir, exist_ok=True)
    save_path = os.path.join(models_dir, f"{model_name}.pkl")

    joblib.dump(model, save_path)
    print(f"✅ تم الحفظ في: {save_path}")

    return model


def train_all_models(X_train, y_train) -> dict:
    """
    يدرّب كل الموديلات ويحفظها.

    Returns:
        dict: اسم الموديل → الموديل المدرّب
    """
    trained = {}
    for name, model in MODELS.items():
        trained[name] = train_model(model, X_train, y_train, name)
    print("\n🎉 تم تدريب كل الموديلات!")
    return trained


def load_model(model_name: str):
    """
    يحمّل موديل محفوظ من الـ disk.
    """
    path = os.path.join(MODELS_DIR, f"{model_name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"الموديل مش موجود: {path}")
    return joblib.load(path)


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from src.data.load_data import load_raw_data
    from src.data.preprocess import run_full_preprocessing

    df = load_raw_data("data/raw/Churn_Modelling.csv")
    X_train, X_test, y_train, y_test, features = run_full_preprocessing(df)
    trained_models = train_all_models(X_train, y_train)
