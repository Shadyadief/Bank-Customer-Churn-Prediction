# 🏦 Bank Customer Churn Prediction

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange?style=for-the-badge&logo=scikit-learn)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-red?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-ff4b4b?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Predict which bank customers are likely to churn — before it's too late.**  
> A full end-to-end Machine Learning project: from raw data to a deployed interactive web app.

---

## 📌 Problem Statement

Customer churn is one of the biggest challenges in the banking industry. Losing a customer costs far more than retaining one. This project builds a **binary classification model** that predicts whether a customer will leave the bank based on their profile and behavior — enabling the bank to take proactive retention actions.

---

## 🎯 Project Highlights

- 📊 **Exploratory Data Analysis** — uncovering churn patterns by geography, age, balance, and more
- 🔧 **Feature Engineering** — creating meaningful new features (Balance/Salary ratio, Age groups, etc.)
- ⚖️ **Class Imbalance Handling** — using SMOTE to balance the training data
- 🤖 **3 ML Models trained & compared** — Logistic Regression, Random Forest, XGBoost
- 🔍 **SHAP Explainability** — understanding *why* the model makes each prediction
- 🌐 **Interactive Streamlit App** — real-time churn prediction with a user-friendly interface
- 🧪 **Unit Tests** — ensuring code reliability
- 🚀 **CI/CD Pipeline** — automated testing and deployment via GitHub Actions

---

## 📁 Project Structure

```
Bank-Customer-Churn-Prediction/
│
├── 📁 data/
│   ├── raw/                    # البيانات الأصلية
│   │   └── Churn_Modelling.csv
│   └── processed/              # البيانات بعد التنظيف
│       └── cleaned_data.csv
│
├── 📁 notebooks/
│   ├── 01_initial_eda.ipynb              # EDA الأولي
│   ├── 02_advanced_eda_feature_eng.ipynb # Feature Engineering
│   └── 03_modeling_evaluation.ipynb      # تدريب وتقييم الموديلات
│
├── 📁 src/
│   ├── data/
│   │   ├── load_data.py        # تحميل البيانات
│   │   └── preprocess.py       # التنظيف والمعالجة
│   ├── features/
│   │   └── build_features.py   # Feature Engineering
│   ├── models/
│   │   ├── train_model.py      # تدريب الموديلات
│   │   ├── predict_model.py    # التنبؤ
│   │   └── evaluate_model.py   # التقييم
│   └── visualization/
│       └── visualize.py        # الرسوم البيانية
│
├── 📁 models/                  # الموديلات المحفوظة (.pkl)
├── 📁 reports/figures/         # الصور والمخططات
├── 📁 app/                     # Streamlit Web App
├── 📁 tests/                   # Unit Tests
├── 📁 docs/                    # التقارير والعروض
│
├── requirements.txt
├── Dockerfile
├── Makefile
└── README.md
```

---

## 📊 Dataset

| Feature | Description |
|--------|-------------|
| `CreditScore` | درجة الائتمان |
| `Geography` | دولة العميل (France / Germany / Spain) |
| `Gender` | الجنس |
| `Age` | العمر |
| `Tenure` | عدد سنوات التعامل مع البنك |
| `Balance` | الرصيد |
| `NumOfProducts` | عدد المنتجات البنكية |
| `HasCrCard` | هل لديه بطاقة ائتمان؟ |
| `IsActiveMember` | هل هو عضو نشط؟ |
| `EstimatedSalary` | الراتب التقديري |
| `Exited` | 🎯 **Target** — هل غادر البنك؟ (1 = نعم، 0 = لا) |

- **Source:** [Kaggle — Churn Modelling Dataset](https://www.kaggle.com/shrutimechlearn/churn-modelling)
- **Size:** 10,000 rows × 14 columns
- **Class Distribution:** ~20% Churn / 80% No Churn (imbalanced)

---

## 🔍 Key EDA Insights

- 🇩🇪 **Germany** has the highest churn rate (~32%) compared to France and Spain
- 👴 **Older customers** (45–60) are significantly more likely to churn
- 💰 Customers with **zero balance** churn at a lower rate
- 📦 Customers with **3–4 products** have extremely high churn rates
- 😴 **Inactive members** are much more likely to leave

---

## 🤖 Models & Results

| Model | Accuracy | ROC-AUC | F1 (Churn) |
|-------|----------|---------|------------|
| Logistic Regression | ~81% | ~0.77 | ~0.57 |
| Random Forest | ~86% | ~0.86 | ~0.71 |
| **XGBoost (Tuned)** ✅ | **~87%** | **~0.88** | **~0.74** |

> ✅ **XGBoost** was selected as the final model based on ROC-AUC and F1-Score for the minority class.

---

## 🔧 Feature Engineering

4 new features were created to boost model performance:

| Feature | Formula | Intuition |
|---------|---------|-----------|
| `Balance_Salary_Ratio` | Balance / EstimatedSalary | مدى اعتماد العميل على رصيده |
| `Products_Per_Tenure` | NumOfProducts / Tenure | مستوى engagement بمرور الوقت |
| `Age_Group` | Binned Age | تأثير العمر بشكل غير خطي |
| `Is_Zero_Balance` | Balance == 0 | flag خاص لعملاء الرصيد الصفري |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Bank-Customer-Churn-Prediction.git
cd Bank-Customer-Churn-Prediction
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run app/app.py
```

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

---

## 🐳 Docker

```bash
docker build -t churn-app .
docker run -p 8501:8501 churn-app
```

---

## 📈 SHAP Explainability

The project uses **SHAP (SHapley Additive exPlanations)** to explain individual predictions:

- **Age** and **NumOfProducts** are the most influential features
- **IsActiveMember** strongly reduces churn probability
- **Geography_Germany** significantly increases churn risk

---

## 🛠️ Tech Stack

| Category | Tools |
|---------|-------|
| Language | Python 3.10+ |
| ML | Scikit-learn, XGBoost, imbalanced-learn |
| Explainability | SHAP |
| Web App | Streamlit |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Containerization | Docker |

---

## 👤 Author

**Your Name**  
[![GitHub](https://img.shields.io/badge/GitHub-your--username-black?style=flat&logo=github)](https://github.com/your-username)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
