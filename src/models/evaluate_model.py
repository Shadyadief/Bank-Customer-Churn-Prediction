import numpy as np # noqa: F401
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)
from sklearn.model_selection import cross_val_score
import os


FIGURES_DIR = "reports/figures"


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """
    يعمل تقييم شامل لموديل واحد.

    Returns:
        dict: النتائج (accuracy, roc_auc, report)
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

    print(f"\n{'='*50}")
    print(f"📊 تقييم: {model_name}")
    print(f"{'='*50}")
    print(classification_report(y_test, y_pred))

    results = {
        "model_name": model_name,
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
    }

    if y_proba is not None:
        auc = roc_auc_score(y_test, y_proba)
        results["roc_auc"] = auc
        print(f"🎯 ROC-AUC Score: {auc:.4f}")

    return results


def plot_confusion_matrix(model, X_test, y_test, model_name: str):
    """يرسم Confusion Matrix ويحفظها."""
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    plt.title(f'Confusion Matrix — {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()

    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"confusion_matrix_{model_name}.png")
    plt.savefig(path)
    plt.close()
    print(f"✅ تم الحفظ: {path}")


def plot_roc_curve(model, X_test, y_test, model_name: str):
    """يرسم ROC Curve ويحفظها."""
    y_proba = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}', color='darkorange', lw=2)
    plt.plot([0, 1], [0, 1], 'k--', lw=1)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve — {model_name}')
    plt.legend(loc='lower right')
    plt.tight_layout()

    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, f"roc_curve_{model_name}.png")
    plt.savefig(path)
    plt.close()
    print(f"✅ تم الحفظ: {path}")


def cross_validate_model(model, X_train, y_train, cv: int = 5) -> dict:
    """يعمل Cross Validation ويرجع النتائج."""
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
    print(f"\n🔁 Cross Validation ({cv} folds):")
    print(f"  Accuracy per fold: {scores.round(3)}")
    print(f"  Mean: {scores.mean():.3f} | Std: {scores.std():.3f}")
    return {"cv_scores": scores, "mean": scores.mean(), "std": scores.std()}


def evaluate_all_models(trained_models: dict, X_test, y_test):
    """يعمل تقييم لكل الموديلات ويطبع مقارنة."""
    all_results = {}
    for name, model in trained_models.items():
        results = evaluate_model(model, X_test, y_test, name)
        plot_confusion_matrix(model, X_test, y_test, name)
        all_results[name] = results

    print("\n📈 مقارنة الموديلات (ROC-AUC):")
    for name, res in all_results.items():
        auc = res.get("roc_auc", "N/A")
        print(f"  {name}: {auc}")

    return all_results
