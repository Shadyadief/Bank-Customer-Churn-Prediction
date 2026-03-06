import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Model Insights", page_icon="📈", layout="wide")

st.title("📈 Model Insights")
st.markdown("مقارنة الموديلات وأهم العوامل المؤثرة في الـ Churn")
st.divider()

# ─── Models Comparison ─────────────────────────────────────────
st.subheader("🤖 مقارنة الموديلات")

models_data = {
    'Model': ['Logistic Regression', 'Random Forest', 'XGBoost (Tuned) ✅'],
    'Accuracy': [81, 86, 87],
    'ROC-AUC': [0.77, 0.86, 0.88],
    'F1-Score (Churn)': [0.57, 0.71, 0.74],
    'Precision': [0.58, 0.72, 0.75],
    'Recall': [0.56, 0.70, 0.73],
}

df_models = pd.DataFrame(models_data)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df_models, x='Model', y='Accuracy',
                 color='Accuracy',
                 color_continuous_scale='Blues',
                 title='Accuracy مقارنة',
                 text='Accuracy')
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[70, 92])
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

# Metrics Table
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

# ─── Feature Importance ────────────────────────────────────────
st.subheader("🔍 Feature Importance")

features_data = {
    'Feature': [
        'Age', 'NumOfProducts', 'IsActiveMember',
        'Balance', 'Geography_Germany', 'CreditScore',
        'Gender_Male', 'Tenure', 'HasCrCard',
        'EstimatedSalary', 'Geography_Spain'
    ],
    'Importance': [0.28, 0.22, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01]
}

df_feat = pd.DataFrame(features_data).sort_values('Importance', ascending=True)

fig = px.bar(df_feat, x='Importance', y='Feature',
             orientation='h',
             color='Importance',
             color_continuous_scale='Viridis',
             title='أهمية كل Feature في قرار الـ Churn')
fig.update_layout(showlegend=False, height=450)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ─── Key Insights ──────────────────────────────────────────────
st.subheader("💡 أهم الـ Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #fff3cd; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #ffc107;">
        <h4>👴 العمر</h4>
        <p>العملاء بين <b>45-60 سنة</b> أكتر الفئات في الـ Churn. ده بيدل إن البنك محتاج يركّز على الفئة العمرية دي بمنتجات مخصصة.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #f8d7da; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #f5576c;">
        <h4>📦 عدد المنتجات</h4>
        <p>العملاء اللي عندهم <b>3-4 منتجات</b> بيغادروا بنسبة عالية جداً! ده counter-intuitive ومحتاج تحقيق.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #d4edda; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #43e97b;">
        <h4>✅ العضوية النشطة</h4>
        <p>العملاء <b>النشطين</b> بيغادروا بنسبة أقل بكتير. تفعيل العضوية وزيادة engagement بيقلل الـ Churn بشكل ملحوظ.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div style="background: #e8f4fd; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #4f46e5;">
        <h4>🇩🇪 ألمانيا</h4>
        <p>عملاء ألمانيا عندهم <b>نسبة Churn ~32%</b> مقارنة بفرنسا وإسبانيا. محتاج استراتيجية خاصة للسوق الألماني.</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div style="background: #f3e8ff; border-radius: 12px; padding: 1.2rem; border-left: 4px solid #764ba2;">
        <h4>💰 الرصيد الصفري</h4>
        <p>العملاء اللي رصيدهم <b>صفر</b> بيغادروا بنسبة أقل! ده ممكن يكون لأنهم بيستخدموا حسابات تشغيلية يومية.</p>
    </div>
    """, unsafe_allow_html=True)
