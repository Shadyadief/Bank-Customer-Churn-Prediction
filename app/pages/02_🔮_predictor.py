import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="Churn Predictor", page_icon="🔮", layout="wide")

# ─── Load Model & Scaler ───────────────────────────────────────
@st.cache_resource
def load_model_and_scaler():
    model  = joblib.load("models/xgboost_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return model, scaler

try:
    model, scaler = load_model_and_scaler()
    model_loaded = True
except Exception:
    model_loaded = False

# ─── Recommendation Engine ────────────────────────────────────
def get_recommendations(customer: dict, prediction: int) -> list:
    """
    بتاخد بيانات العميل والـ prediction
    وبترجع عروض مخصصة لو العميل هيسيب
    """
    if prediction == 0:
        return []

    offers = []

    if customer['IsActiveMember'] == 0:
        offers.append({
            'icon': '🎁',
            'title': 'CashBack Activation Offer',
            'desc': 'احصل على 5% cashback لمدة 3 شهور عند تفعيل حسابك',
            'color': '#fff3cd',
            'border': '#ffc107',
        })

    if customer['NumOfProducts'] == 1:
        offers.append({
            'icon': '💳',
            'title': 'Premium Credit Card — Free First Year',
            'desc': 'بطاقة ائتمان مجانية السنة الأولى مع مزايا حصرية',
            'color': '#e8f4fd',
            'border': '#4f46e5',
        })

    if customer['Balance'] > 100_000:
        offers.append({
            'icon': '📈',
            'title': 'High-Yield Savings Account',
            'desc': 'فائدة 8% سنوياً على الأرصدة فوق 100,000',
            'color': '#d4edda',
            'border': '#28a745',
        })
    elif customer['Balance'] > 0:
        offers.append({
            'icon': '💰',
            'title': 'Savings Boost Plan',
            'desc': 'فائدة 5% على رصيدك الحالي لمدة 6 شهور',
            'color': '#d4edda',
            'border': '#43e97b',
        })

    if customer['Age'] > 50:
        offers.append({
            'icon': '🏦',
            'title': 'Retirement Investment Plan',
            'desc': 'خطة ادخار للتقاعد بعوائد مضمونة',
            'color': '#f3e8ff',
            'border': '#764ba2',
        })

    if customer['HasCrCard'] == 0:
        offers.append({
            'icon': '💳',
            'title': 'First Credit Card — Zero Fees',
            'desc': 'بطاقة ائتمان بدون رسوم سنوية للسنة الأولى',
            'color': '#e8f4fd',
            'border': '#4facfe',
        })

    if customer['Geography_Germany'] == 1:
        offers.append({
            'icon': '🇩🇪',
            'title': 'Loyalty Reward — Germany Exclusive',
            'desc': 'برنامج نقاط مضاعفة حصري لعملاء ألمانيا',
            'color': '#fff3cd',
            'border': '#ffc107',
        })

    if not offers:
        offers.append({
            'icon': '⭐',
            'title': 'VIP Loyalty Program',
            'desc': 'انضم لبرنامج VIP واحصل على مزايا حصرية',
            'color': '#f8d7da',
            'border': '#f5576c',
        })

    return offers


# ─── Header ───────────────────────────────────────────────────
st.title("🔮 Churn Predictor")
st.markdown("أدخل بيانات العميل وشوف هيبقى Churn ولا لأ")
st.divider()

if not model_loaded:
    st.warning("⚠️ الموديل مش موجود! شغّل `python train_model.py` الأول.")
    st.code("python train_model.py", language="bash")
    st.stop()

# ─── Input Form ───────────────────────────────────────────────
st.subheader("📝 بيانات العميل")

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.slider("💳 Credit Score", 300, 850, 650)
    age          = st.slider("🎂 Age", 18, 92, 35)
    tenure       = st.slider("📅 Tenure (years)", 0, 10, 5)
    balance      = st.number_input("💰 Balance", 0.0, 250_000.0, 50_000.0, 1_000.0)

with col2:
    num_products = st.selectbox("📦 Num of Products", [1, 2, 3, 4])
    has_cr_card  = st.selectbox("💳 Has Credit Card?", ["Yes", "No"])
    is_active    = st.selectbox("✅ Is Active Member?", ["Yes", "No"])
    salary       = st.number_input("💵 Estimated Salary", 0.0, 200_000.0, 75_000.0, 1_000.0)

with col3:
    geography = st.selectbox("🌍 Geography", ["France", "Germany", "Spain"])
    gender    = st.selectbox("👤 Gender", ["Male", "Female"])

# ─── Predict ──────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict Churn", type="primary", use_container_width=True)

if predict_btn:
    input_dict = {
        'CreditScore':        credit_score,
        'Age':                age,
        'Tenure':             tenure,
        'Balance':            balance,
        'NumOfProducts':      num_products,
        'HasCrCard':          1 if has_cr_card == "Yes" else 0,
        'IsActiveMember':     1 if is_active   == "Yes" else 0,
        'EstimatedSalary':    salary,
        'Gender_Male':        1 if gender    == "Male"    else 0,
        'Geography_Germany':  1 if geography == "Germany" else 0,
        'Geography_Spain':    1 if geography == "Spain"   else 0,
    }

    input_df     = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)

    prediction  = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    st.divider()
    st.subheader("📊 النتيجة")

    col_res, col_gauge = st.columns(2)

    # ── Result Card ──
    with col_res:
        if prediction == 1:
            st.error(f"## 🔴 سيغادر البنك (Churn)")
        else:
            st.success(f"## 🟢 سيبقى مع البنك (No Churn)")

        st.markdown(f"### احتمالية المغادرة: **{probability*100:.1f}%**")

        # Risk badge
        if probability >= 0.7:
            st.markdown("🚨 **خطر عالي** — يحتاج تدخل فوري")
        elif probability >= 0.5:
            st.markdown("⚠️ **خطر متوسط** — راقبه عن كثب")
        else:
            st.markdown("✅ **خطر منخفض** — العميل مستقر")

    # ── Gauge Chart ──
    with col_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={'text': "Churn Probability %", 'font': {'size': 16}},
            number={'suffix': '%', 'font': {'size': 36}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#f5576c" if probability > 0.5 else "#43e97b"},
                'steps': [
                    {'range': [0,  30], 'color': '#d4edda'},
                    {'range': [30, 60], 'color': '#fff3cd'},
                    {'range': [60, 100], 'color': '#f8d7da'},
                ],
                'threshold': {
                    'line': {'color': 'black', 'width': 3},
                    'thickness': 0.75,
                    'value': 50,
                }
            }
        ))
        fig.update_layout(height=280, margin=dict(t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Recommendations ──
    st.divider()
    recommendations = get_recommendations(input_dict, prediction)

    if prediction == 1 and recommendations:
        st.subheader("💡 عروض مخصصة لإقناعه يفضل")
        st.caption(f"تم اقتراح {len(recommendations)} عرض بناءً على بيانات العميل")

        cols = st.columns(min(len(recommendations), 3))
        for i, offer in enumerate(recommendations):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="
                    background: {offer['color']};
                    border-radius: 12px;
                    padding: 1.2rem;
                    border-left: 4px solid {offer['border']};
                    margin-bottom: 1rem;
                    min-height: 110px;
                ">
                    <h4 style="margin:0 0 0.4rem 0">{offer['icon']} {offer['title']}</h4>
                    <p style="margin:0; font-size:0.9rem; color:#444">{offer['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

    elif prediction == 0:
        st.subheader("💡 التوصيات")
        st.markdown("""
        <div style="background:#d4edda; border-radius:12px; padding:1.2rem; border-left:4px solid #43e97b;">
            <h4>✅ العميل مستقر — ركّز على الـ Engagement</h4>
            <ul>
                <li>🌟 قدّم له برنامج loyalty points</li>
                <li>📈 اقترح منتجات إضافية مناسبة</li>
                <li>📬 راسله بعروض دورية عشان يفضل نشط</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
