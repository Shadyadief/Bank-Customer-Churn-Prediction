import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EDA Dashboard", page_icon="📊", layout="wide")

# ─── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/Churn_Modelling.csv")
    df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
    return df

df = load_data()

# ─── Header ────────────────────────────────────────────────────
st.title("📊 EDA Dashboard")
st.markdown("استكشاف البيانات وفهم patterns الـ Churn")
st.divider()

# ─── Quick Stats ───────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("إجمالي العملاء", f"{len(df):,}")
col2.metric("عملاء غادروا", f"{df['Exited'].sum():,}", f"{df['Exited'].mean()*100:.1f}%")
col3.metric("عملاء بقوا", f"{(df['Exited']==0).sum():,}")
col4.metric("متوسط العمر", f"{df['Age'].mean():.0f} سنة")

st.divider()

# ─── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Geography", "👥 Demographics", "💰 Financial", "🔗 Correlation"])

# ── Tab 1: Geography ──
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn by Geography")
        fig = px.histogram(df, x='Geography', color='Exited',
                          barmode='group',
                          color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                          labels={'Exited': 'Churn'},
                          title='عدد العملاء حسب الدولة')
        fig.update_layout(legend_title="Churn")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Churn Rate by Geography")
        churn_geo = df.groupby('Geography')['Exited'].mean().reset_index()
        churn_geo['Churn Rate %'] = (churn_geo['Exited'] * 100).round(1)
        fig2 = px.bar(churn_geo, x='Geography', y='Churn Rate %',
                      color='Churn Rate %',
                      color_continuous_scale='RdYlGn_r',
                      title='نسبة الـ Churn لكل دولة')
        st.plotly_chart(fig2, use_container_width=True)

# ── Tab 2: Demographics ──
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn by Age")
        fig = px.box(df, x='Exited', y='Age',
                     color='Exited',
                     color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                     labels={'Exited': 'Churn'},
                     title='توزيع العمر حسب الـ Churn')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Churn by Gender")
        fig = px.histogram(df, x='Gender', color='Exited',
                          barmode='group',
                          color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                          title='الـ Churn حسب الجنس')
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Churn by NumOfProducts")
        fig = px.histogram(df, x='NumOfProducts', color='Exited',
                          barmode='group',
                          color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                          title='الـ Churn حسب عدد المنتجات')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Active Member vs Churn")
        fig = px.histogram(df, x='IsActiveMember', color='Exited',
                          barmode='group',
                          color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                          title='العضوية النشطة والـ Churn')
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 3: Financial ──
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn by Balance")
        fig = px.box(df, x='Exited', y='Balance',
                     color='Exited',
                     color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                     title='توزيع الرصيد حسب الـ Churn')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Churn by Credit Score")
        fig = px.box(df, x='Exited', y='CreditScore',
                     color='Exited',
                     color_discrete_map={0: '#4f46e5', 1: '#f5576c'},
                     title='درجة الائتمان والـ Churn')
        st.plotly_chart(fig, use_container_width=True)

# ── Tab 4: Correlation ──
with tab4:
    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt='.2f',
                cmap='coolwarm', ax=ax, linewidths=0.5)
    plt.title('Correlation Heatmap', fontsize=14)
    st.pyplot(fig)

# ─── Raw Data ──────────────────────────────────────────────────
st.divider()
with st.expander("🗃️ شوف البيانات الخام"):
    st.dataframe(df, use_container_width=True)
    st.caption(f"Shape: {df.shape}")
