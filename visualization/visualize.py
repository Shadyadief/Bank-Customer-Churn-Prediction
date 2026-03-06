import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import os

FIGURES_DIR = "reports/figures"


def plot_churn_by_geography(df: pd.DataFrame):
    """رسم Churn حسب الدولة."""
    plt.figure(figsize=(8, 5))
    sns.countplot(x='Geography', hue='Exited', data=df, palette='Set2')
    plt.title('Churn by Geography')
    plt.xlabel('Geography')
    plt.ylabel('Count')
    plt.tight_layout()
    _save_fig("churn_by_geography.png")


def plot_churn_by_age(df: pd.DataFrame):
    """رسم Churn حسب العمر."""
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Exited', y='Age', data=df, palette='Set2')
    plt.title('Churn by Age')
    plt.xlabel('Exited')
    plt.ylabel('Age')
    plt.tight_layout()
    _save_fig("churn_by_age.png")


def plot_churn_by_balance(df: pd.DataFrame):
    """رسم Churn حسب الرصيد."""
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Exited', y='Balance', data=df, palette='Set2')
    plt.title('Churn by Balance')
    plt.xlabel('Exited')
    plt.ylabel('Balance')
    plt.tight_layout()
    _save_fig("churn_by_balance.png")


def plot_correlation_heatmap(df: pd.DataFrame):
    """رسم Correlation Heatmap."""
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt='.2f', cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    _save_fig("correlation_heatmap.png")


def plot_feature_importance(model, feature_names: list, model_name: str = "model"):
    """رسم Feature Importance للـ Tree-based Models."""
    if not hasattr(model, 'feature_importances_'):
        print("⚠️ الموديل ده مش بيعمل feature_importances_")
        return

    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
    plt.title(f'Feature Importance — {model_name}')
    plt.tight_layout()
    _save_fig(f"feature_importance_{model_name}.png")


def plot_shap_summary(model, X_test, feature_names: list):
    """رسم SHAP Summary Plot."""
    print("🔍 بيحسب SHAP values...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    plt.figure()
    shap.summary_plot(shap_values, X_test, feature_names=feature_names, show=False)
    _save_fig("shap_summary.png")

    plt.figure()
    shap.summary_plot(shap_values, X_test, feature_names=feature_names,
                      plot_type='bar', show=False)
    _save_fig("shap_bar.png")


def _save_fig(filename: str):
    """Helper بيحفظ الـ figure."""
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"✅ تم الحفظ: {path}")


def run_all_eda_plots(df: pd.DataFrame):
    """يشغّل كل رسومات الـ EDA دفعة واحدة."""
    print("📊 بيرسم كل الـ EDA plots...")
    plot_churn_by_geography(df)
    plot_churn_by_age(df)
    plot_churn_by_balance(df)
    plot_correlation_heatmap(df)
    print("✅ انتهى رسم كل الـ EDA plots!")
