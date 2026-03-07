from setuptools import setup, find_packages

setup(
    name="bank-churn-prediction",
    version="1.0.0",
    author="Shady Adief",
    description="Bank Customer Churn Prediction — End-to-End ML Project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "imbalanced-learn",
        "shap",
        "matplotlib",
        "seaborn",
        "streamlit",
        "plotly",
        "joblib",
    ],
)
