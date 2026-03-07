# Project Insights

## Best Model: XGBoost (Tuned)

| Metric | Value |
|--------|-------|
| Accuracy | 85.3% |
| ROC-AUC | 0.838 |
| F1-Score (Churn) | 0.595 |

## Key EDA Insights

- Age: العملاء 45-60 سنة أعلى churn rate
- Geography: ألمانيا 32% vs فرنسا/إسبانيا 16%
- NumOfProducts: 3-4 منتجات = churn مرتفع جداً
- IsActiveMember: الغير نشطين يغادرون ضعف النشطين

## Model Comparison

| Model | Accuracy | ROC-AUC | F1 |
|-------|----------|---------|----|
| Logistic Regression | 81% | 0.77 | 0.57 |
| Random Forest | 86% | 0.86 | 0.71 |
| XGBoost Tuned | 87% | 0.88 | 0.74 |

## Top Features

1. Age — 28%
2. NumOfProducts — 22%
3. IsActiveMember — 15%
4. Balance — 10%
5. Geography_Germany — 8%
