import numpy as np  # noqa: F401
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
)
from sklearn.model_selection import cross_val_score

FIGURES_DIR = "reports/figures"
MODELS_DIR  = "models"


# ─── Single Model Evaluation ───────────────────────────────────────────────────
def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """
    يعمل تقييم شامل لموديل واحد.
    Returns:
        dict: النتائج (accuracy, roc_auc, f1, precision, recall, report)
    """
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    acc       = accuracy_score(y_test, y_pred)
    f1        = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall    = recall_score(y_test, y_pred)
    auc       = roc_auc_score(y_test, y_proba) if y_proba is not None else None

    print(f"\n{'='*50}")
    print(f"📊 تقييم: {model_name}")
    print(f"{'='*50}")
    print(classification_report(y_test, y_pred))
    if auc:
        print(f"🎯 ROC-AUC Score: {auc:.4f}")

    results = {
        "model_name":             model_name,
        "classification_report":  classification_report(y_test, y_pred, output_dict=True),
        "Accuracy":               round(acc,       4),
        "ROC-AUC":                round(auc,       4) if auc else None,
        "F1-Score (Churn)":       round(f1,        4),
        "Precision":              round(precision, 4),
        "Recall":                 round(recall,    4),
    }
    return results


# ─── Confusion Matrix ──────────────────────────────────────────────────────────
def plot_confusion_matrix(model, X_test, y_test, model_name: str):
    """يرسم Confusion Matrix ويحفظها."""
    y_pred = model.predict(X_test)
    cm     = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn", "Churn"],
                yticklabels=["No Churn", "Churn"])
    plt.title(f"Confusion Matrix — {model_name}")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()

    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"confusion_matrix_{model_name}.png")
    plt.savefig(path)
    plt.close()
    print(f"✅ تم الحفظ: {path}")


# ─── ROC Curve ─────────────────────────────────────────────────────────────────
def plot_roc_curve(model, X_test, y_test, model_name: str):
    """يرسم ROC Curve ويحفظها."""
    y_proba = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}", color="darkorange", lw=2)
    plt.plot([0, 1], [0, 1], "k--", lw=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve — {model_name}")
    plt.legend(loc="lower right")
    plt.tight_layout()

    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"roc_curve_{model_name}.png")
    plt.savefig(path)
    plt.close()
    print(f"✅ تم الحفظ: {path}")


# ─── Cross Validation ──────────────────────────────────────────────────────────
def cross_validate_model(model, X_train, y_train, cv: int = 5) -> dict:
    """يعمل Cross Validation ويرجع النتائج."""
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")
    print(f"\n🔁 Cross Validation ({cv} folds):")
    print(f"  Accuracy per fold: {scores.round(3)}")
    print(f"  Mean: {scores.mean():.3f} | Std: {scores.std():.3f}")
    return {"cv_scores": scores, "mean": scores.mean(), "std": scores.std()}


# ─── Feature Importance Extractor ─────────────────────────────────────────────
def extract_feature_importance(model, feature_names: list) -> dict:
    """
    يستخرج feature importance من الموديل لو موجودة.
    يشتغل مع XGBoost و RandomForest.
    """
    if hasattr(model, "feature_importances_"):
        importance = dict(zip(feature_names, model.feature_importances_.tolist()))
        # ترتيب تنازلي
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        return importance
    return {}


# ─── Evaluate All + Save PKL ───────────────────────────────────────────────────
def evaluate_all_models(trained_models: dict, X_test, y_test,
                        feature_names: list = None,
                        best_model_name: str = "xgboost_model"):
    """
    يعمل تقييم لكل الموديلات، يطبع مقارنة،
    ويحفظ model_metrics.pkl و feature_importance.pkl.

    Parameters:
        trained_models  : dict {name: model}
        X_test / y_test : بيانات الاختبار
        feature_names   : أسماء الـ features (للـ feature importance)
        best_model_name : اسم الموديل اللي هنحفظ feature importance بتاعته
    """
    all_results  = {}
    metrics_list = []

    for name, model in trained_models.items():
        results = evaluate_model(model, X_test, y_test, name)
        plot_confusion_matrix(model, X_test, y_test, name)
        all_results[name] = results

        # ── صف واحد في جدول المقارنة ──
        metrics_list.append({
            "Model":            name.replace("_", " ").title(),
            "Accuracy":         results["Accuracy"],
            "ROC-AUC":          results["ROC-AUC"],
            "F1-Score (Churn)": results["F1-Score (Churn)"],
            "Precision":        results["Precision"],
            "Recall":           results["Recall"],
        })

    # ── طباعة مقارنة ──
    print("\n📈 مقارنة الموديلات:")
    for row in metrics_list:
        print(f"  {row['Model']:30} Acc={row['Accuracy']} | AUC={row['ROC-AUC']} | F1={row['F1-Score (Churn)']}")

    # ── حفظ model_metrics.pkl ──
    os.makedirs(MODELS_DIR, exist_ok=True)
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.pkl")
    joblib.dump(metrics_list, metrics_path)
    print(f"\n✅ تم حفظ model_metrics.pkl في: {metrics_path}")

    # ── حفظ feature_importance.pkl من أفضل موديل ──
    if feature_names and best_model_name in trained_models:
        best_model  = trained_models[best_model_name]
        feat_imp    = extract_feature_importance(best_model, feature_names)
        if feat_imp:
            feat_path = os.path.join(MODELS_DIR, "feature_importance.pkl")
            joblib.dump(feat_imp, feat_path)
            print(f"✅ تم حفظ feature_importance.pkl في: {feat_path}")
        else:
            print("⚠️ الموديل مش عنده feature_importances_")
    else:
        print("⚠️ feature_names مش متاحة — feature_importance.pkl مش هيتحفظ")

    return all_results


# ─── Main (للتشغيل المباشر) ────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.append(".")

    from src.data.load_data       import load_raw_data
    from src.data.preprocess      import run_full_preprocessing
    from src.models.train_model   import train_all_models

    df = load_raw_data("data/raw/Churn_Modelling.csv")
    X_train, X_test, y_train, y_test, features = run_full_preprocessing(df)

    # تدريب
    trained_models = train_all_models(X_train, y_train)

    # تقييم + حفظ
    evaluate_all_models(
        trained_models,
        X_test,
        y_test,
        feature_names   = features,
        best_model_name = "xgboost_model",
    )

    print("\n🎉 كل حاجة اتحفظت جوه models/")
