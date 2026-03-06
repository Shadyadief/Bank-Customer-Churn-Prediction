import streamlit as st

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
    <style>
        .main-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #1a1a2e;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .sub-title {
            font-size: 1.1rem;
            color: #555;
            text-align: center;
            margin-bottom: 2rem;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 5px solid #4f46e5;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 16px;
            padding: 1.5rem;
            color: white;
            text-align: center;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
        }
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.85;
        }
    </style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────
st.markdown('<div class="main-title">🏦 Bank Customer Churn Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">End-to-end Machine Learning project to predict which customers are likely to leave the bank</div>', unsafe_allow_html=True)

st.divider()

# ─── Project Overview ──────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-value">10K</div>
            <div class="metric-label">📊 Customers</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-value">87%</div>
            <div class="metric-label">🎯 Accuracy</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="metric-value">0.88</div>
            <div class="metric-label">📈 ROC-AUC</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="metric-value">3</div>
            <div class="metric-label">🤖 Models</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Navigation Cards ──────────────────────────────────────────
st.subheader("🗺️ استكشف المشروع")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card">
            <h3>📊 EDA Dashboard</h3>
            <p>استكشاف البيانات وفهم patterns الـ Churn من خلال رسوم بيانية تفاعلية</p>
            <ul>
                <li>توزيع العملاء</li>
                <li>Churn by Geography & Age</li>
                <li>Correlation Heatmap</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card" style="border-left-color: #f5576c;">
            <h3>🔮 Churn Predictor</h3>
            <p>أدخل بيانات عميل وشوف هيبقى Churn ولا لأ في الحال</p>
            <ul>
                <li>Real-time prediction</li>
                <li>Churn probability</li>
                <li>SHAP explanation</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card" style="border-left-color: #43e97b;">
            <h3>📈 Model Insights</h3>
            <p>مقارنة الموديلات وفهم أهم العوامل المؤثرة في الـ Churn</p>
            <ul>
                <li>Models comparison</li>
                <li>Feature importance</li>
                <li>SHAP summary</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ─── Tech Stack ────────────────────────────────────────────────
st.subheader("🛠️ Tech Stack")

techs = ["Python", "XGBoost", "Scikit-learn", "SMOTE", "SHAP", "Streamlit", "Pandas", "Seaborn"]
cols = st.columns(len(techs))
for col, tech in zip(cols, techs):
    col.markdown(f"""
        <div style="background:#f0f2f6; border-radius:8px; padding:0.5rem; text-align:center; font-weight:600; font-size:0.85rem;">
            {tech}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
    st.title("🏦 Churn Prediction")
    st.markdown("---")
    st.markdown("### 📌 Navigation")
    st.markdown("👈 اختار من القائمة على اليسار")
    st.markdown("---")
    st.markdown("### 👤 Made by")
    st.markdown("**Shady Adief**")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Shadyadief-black?logo=github)](https://github.com/Shadyadief)")
    st.markdown("---")
    st.markdown("### 📊 Dataset")
    st.markdown("Churn Modelling Dataset")
    st.markdown("10,000 customers | 14 features")
