import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

# ─── Paths ─────────────────────────────────────────────────────────────────────
MODELS_DIR = "models"

# ─── Model Configs ─────────────────────────────────────────────────────────────
MODELS = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
    ),
    "XGBoost": XGBClassifier(
        learning_rate=0.2,
        max_depth=7,
        n_estimators=300,
        subsample=0.8,
        random_state=42,
        eval_metric="logloss",
        verbosity=0,
    ),
}

# ── اسم الموديل الـ key للـ pkl ──
MODEL_FILENAMES = {
    "Logistic Regression": "logistic_regression",
    "Random Forest":       "random_forest",
    "XGBoost":             "xgboost_model",
}


# ─── Train Single Model ────────────────────────────────────────────────────────
def train_model(model, X_train, y_train,
                model_name: str,
                models_dir: str = MODELS_DIR) -> object:
    """
    يدرّب موديل واحد ويحفظه.

    Returns:
        الموديل بعد التدريب
    """
    print(f"🚀 بيدرّب: {model_name}...")
    model.fit(X_train, y_train)

    os.makedirs(models_dir, exist_ok=True)
    filename  = MODEL_FILENAMES.get(model_name, model_name.lower().replace(" ", "_"))
    save_path = os.path.join(models_dir, f"{filename}.pkl")
    joblib.dump(model, save_path)
    print(f"✅ تم الحفظ في: {save_path}")
    return model


# ─── Train All Models ──────────────────────────────────────────────────────────
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


# ─── Load Single Model ─────────────────────────────────────────────────────────
def load_model(model_name: str) -> object:
    """
    يحمّل موديل محفوظ من الـ disk.

    Parameters:
        model_name: الاسم المختصر  e.g. "xgboost_model"
    """
    path = os.path.join(MODELS_DIR, f"{model_name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"الموديل مش موجود: {path}")
    return joblib.load(path)


# ─── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.append(".")

    from src.data.load_data      import load_raw_data
    from src.data.preprocess     import run_full_preprocessing
    from src.models.evaluate_model import evaluate_all_models

    # 1. تحميل البيانات
    print("📂 تحميل البيانات...")
    df = load_raw_data("data/raw/Churn_Modelling.csv")

    # 2. معالجة
    print("🔧 معالجة البيانات...")
    X_train, X_test, y_train, y_test, features = run_full_preprocessing(df)

    # 3. تدريب
    trained_models = train_all_models(X_train, y_train)

    # 4. تقييم + حفظ model_metrics.pkl + feature_importance.pkl  ← الجزء المهم
    print("\n📊 تقييم الموديلات وحفظ النتائج...")
    evaluate_all_models(
        trained_models  = trained_models,
        X_test          = X_test,
        y_test          = y_test,
        feature_names   = features,
        best_model_name = "XGBoost",
    )

    print("\n✅ كل حاجة جاهزة في models/")
    print("   ├── logistic_regression.pkl")
    print("   ├── random_forest.pkl")
    print("   ├── xgboost_model.pkl")
    print("   ├── model_metrics.pkl       ← للـ insights page")
    print("   └── feature_importance.pkl  ← للـ insights page")
