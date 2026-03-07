import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os

st.set_page_config(page_title="Model Insights", page_icon="📈", layout="wide")

st.title("📈 Model Insights")
st.markdown("مقارنة الموديلات وأهم العوامل المؤثرة في الـ Churn")
st.divider()

# ─── Load Real Metrics ────────────────────────────────────────
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_metrics():
    try:
        metrics  = joblib.load(os.path.join(_BASE_DIR, "models", "model_metrics.pkl"))
        feat_imp = joblib.load(os.path.join(_BASE_DIR, "models", "feature_importance.pkl"))
        return pd.DataFrame(metrics), feat_imp, True
    except Exception:
        return None, None, False

df_models, feat_importance, loaded = load_metrics()

if not loaded:
    st.warning("⚠️ ملفات الموديل مش موجودة! شغّل `python train_model.py` الأول.")
    st.code("python train_model.py", language="bash")
    st.stop()

# ─── Models Comparison ────────────────────────────────────────
st.subheader("🤖 مقارنة الموديلات")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df_models, x='Model', y='Accuracy',
                 color='Accuracy',
                 color_continuous_scale='Blues',
                 title='Accuracy مقارنة',
                 text='Accuracy')
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[70, 95])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df_models, x='Model', y='ROC-AUC',
                 color='ROC-AUC',
                 color_continuous_scale='Purples',
                 title='ROC-AUC مقارنة',
                 text='ROC-AUC')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0.6, 0.95])
    st.plotly_chart(fig, use_container_width=True)

# ── Metrics Table ──
st.markdown("### 📊 جدول المقارنة الكامل")
st.dataframe(
    df_models.style.highlight_max(
        subset=['Accuracy', 'ROC-AUC', 'F1-Score (Churn)'],
        color='#d4edda'
    ),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ─── Feature Importance ───────────────────────────────────────
st.subheader("🔍 Feature Importance — XGBoost")

df_feat = pd.DataFrame({
    'Feature':    list(feat_importance.keys()),
    'Importance': list(feat_importance.values()),
}).sort_values('Importance', ascending=True)

fig = px.bar(df_feat, x='Importance', y='Feature',
             orientation='h',
             color='Importance',
             color_continuous_scale='Viridis',
             title='أهمية كل Feature في قرار الـ Churn')
fig.update_layout(showlegend=False, height=450)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─── Key Insights ─────────────────────────────────────────────
st.subheader("💡 أهم الـ Insights")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background:#fff3cd;border-radius:12px;padding:1.2rem;border-left:4px solid #ffc107;">
        <h4>👴 العمر</h4>
        <p>العملاء بين <b>45-60 سنة</b> أكتر الفئات في الـ Churn. البنك محتاج منتجات مخصصة ليهم.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="background:#f8d7da;border-radius:12px;padding:1.2rem;border-left:4px solid #f5576c;">
        <h4>📦 عدد المنتجات</h4>
        <p>العملاء اللي عندهم <b>3-4 منتجات</b> بيغادروا بنسبة عالية — ظاهرة counter-intuitive محتاجة تحقيق.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div style="background:#d4edda;border-radius:12px;padding:1.2rem;border-left:4px solid #43e97b;">
        <h4>✅ العضوية النشطة</h4>
        <p>العملاء <b>النشطين</b> بيغادروا بنسبة أقل بكتير. زيادة الـ engagement بيقلل الـ Churn.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5 = st.columns(2)
with col4:
    st.markdown("""
    <div style="background:#e8f4fd;border-radius:12px;padding:1.2rem;border-left:4px solid #4f46e5;">
        <h4>🇩🇪 ألمانيا</h4>
        <p>عملاء ألمانيا عندهم <b>نسبة Churn ~32%</b> مقارنة بفرنسا وإسبانيا — محتاج استراتيجية خاصة.</p>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div style="background:#f3e8ff;border-radius:12px;padding:1.2rem;border-left:4px solid #764ba2;">
        <h4>💰 الرصيد الصفري</h4>
        <p>العملاء اللي رصيدهم <b>صفر</b> بيغادروا بنسبة أقل — غالباً بيستخدموا حسابات تشغيلية يومية.</p>
    </div>
    """, unsafe_allow_html=True)
