import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="Churn Predictor", page_icon="🔮", layout="wide")

# ─── Load Model & Scaler ───────────────────────────────────────
@st.cache_resource
def load_model_and_scaler():
    model = joblib.load("models/xgboost_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler

try:
    model, scaler = load_model_and_scaler()
    model_loaded = True
except:
    model_loaded = False

# ─── Header ────────────────────────────────────────────────────
st.title("🔮 Churn Predictor")
st.markdown("أدخل بيانات العميل وشوف هيبقى Churn ولا لأ")
st.divider()

if not model_loaded:
    st.warning("⚠️ الموديل مش موجود! تأكد إنك دربت الموديل الأول وإن الملفات موجودة في `models/`")
    st.stop()

# ─── Input Form ────────────────────────────────────────────────
st.subheader("📝 بيانات العميل")

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.slider("💳 Credit Score", 300, 850, 650)
    age = st.slider("🎂 Age", 18, 92, 35)
    tenure = st.slider("📅 Tenure (years)", 0, 10, 5)
    balance = st.number_input("💰 Balance", min_value=0.0, max_value=250000.0, value=50000.0, step=1000.0)

with col2:
    num_products = st.selectbox("📦 Num of Products", [1, 2, 3, 4])
    has_cr_card = st.selectbox("💳 Has Credit Card?", ["Yes", "No"])
    is_active = st.selectbox("✅ Is Active Member?", ["Yes", "No"])
    salary = st.number_input("💵 Estimated Salary", min_value=0.0, max_value=200000.0, value=75000.0, step=1000.0)

with col3:
    geography = st.selectbox("🌍 Geography", ["France", "Germany", "Spain"])
    gender = st.selectbox("👤 Gender", ["Male", "Female"])

# ─── Predict Button ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Churn", type="primary", use_container_width=True)

if predict_btn:
    # بناء الـ input
    input_dict = {
        'CreditScore': credit_score,
        'Age': age,
        'Tenure': tenure,
        'Balance': balance,
        'NumOfProducts': num_products,
        'HasCrCard': 1 if has_cr_card == "Yes" else 0,
        'IsActiveMember': 1 if is_active == "Yes" else 0,
        'EstimatedSalary': salary,
        'Gender_Male': 1 if gender == "Male" else 0,
        'Geography_Germany': 1 if geography == "Germany" else 0,
        'Geography_Spain': 1 if geography == "Spain" else 0,
    }

    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.divider()
    st.subheader("📊 النتيجة")

    col1, col2 = st.columns(2)

    with col1:
        if prediction == 1:
            st.error("## 🔴 سيغادر البنك (Churn)")
            st.markdown(f"### احتمالية المغادرة: **{probability*100:.1f}%**")
        else:
            st.success("## 🟢 سيبقى مع البنك (No Churn)")
            st.markdown(f"### احتمالية المغادرة: **{probability*100:.1f}%**")

        # Recommendations
        st.markdown("---")
        st.markdown("### 💡 التوصيات")
        if prediction == 1:
            st.markdown("""
            - 📞 تواصل مع العميل فوراً
            - 🎁 قدّم له عرض خاص أو مزايا إضافية
            - 🔍 افهم سبب عدم رضاه
            - 💳 اقترح منتجات مناسبة لاحتياجاته
            """)
        else:
            st.markdown("""
            - ✅ العميل راضي ومستمر
            - 🌟 قدّم له برامج loyalty
            - 📈 اقترح منتجات إضافية لزيادة engagement
            """)

    with col2:
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=probability * 100,
            title={'text': "Churn Probability %", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#f5576c" if probability > 0.5 else "#43e97b"},
                'steps': [
                    {'range': [0, 30], 'color': '#d4edda'},
                    {'range': [30, 60], 'color': '#fff3cd'},
                    {'range': [60, 100], 'color': '#f8d7da'},
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
