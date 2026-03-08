import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDA Dashboard | Bank Churn",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Spider + CSS ──────────────────────────────────────────────────────────────
from spider import spider
spider()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ─── Theme colors from session ─────────────────────────────────────────────────
THEME = st.session_state.get("theme", "dark")
LANG  = st.session_state.get("lang",  "en")

COLORS = {
    "dark":  {"stayed": "#00d4ff", "churned": "#f43f5e", "bg": "#111827", "grid": "#1e293b", "text": "#94a3b8"},
    "light": {"stayed": "#0369a1", "churned": "#e11d48", "bg": "#ffffff", "grid": "#e2e8f0", "text": "#475569"},
}
C = COLORS[THEME]

PLOTLY_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = dict(family="DM Mono, monospace", color=C["text"], size=12),
    title_font    = dict(family="Syne, sans-serif",   color=C["text"], size=15),
    xaxis         = dict(gridcolor=C["grid"], linecolor=C["grid"], tickfont=dict(color=C["text"])),
    yaxis         = dict(gridcolor=C["grid"], linecolor=C["grid"], tickfont=dict(color=C["text"])),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"])),
    margin        = dict(l=20, r=20, t=50, b=20),
)

# ─── Translations ──────────────────────────────────────────────────────────────
T = {
    "en": {
        "title":         "📊 EDA Dashboard",
        "subtitle":      "Exploratory Data Analysis — Understanding Churn Patterns",
        "total":         "Total Customers",
        "churned":       "Churned",
        "retained":      "Retained",
        "avg_age":       "Avg Age",
        "avg_balance":   "Avg Balance",
        "avg_credit":    "Avg Credit Score",
        "tab_geo":       "🌍 Geography",
        "tab_demo":      "👥 Demographics",
        "tab_fin":       "💰 Financial",
        "tab_corr":      "🔗 Correlation",
        "tab_raw":       "🗃️ Raw Data",
        "churn_geo":     "Churn Count by Geography",
        "churn_rate_geo":"Churn Rate % by Geography",
        "age_dist":      "Age Distribution by Churn",
        "gender_churn":  "Churn by Gender",
        "products_churn":"Churn by Number of Products",
        "active_churn":  "Active Member vs Churn",
        "balance_dist":  "Balance Distribution by Churn",
        "credit_dist":   "Credit Score Distribution by Churn",
        "salary_dist":   "Estimated Salary by Churn",
        "tenure_churn":  "Tenure (Years) by Churn",
        "corr_title":    "Correlation Heatmap",
        "corr_sub":      "Numeric feature correlations with Churn",
        "raw_title":     "Raw Dataset",
        "shape":         "Shape",
        "stayed":        "Stayed",
        "churned_lbl":   "Churned",
        "churn_insight": "Key Insight",
        "years":         "years",
    },
    "ar": {
        "title":         "📊 لوحة التحليل الاستكشافي",
        "subtitle":      "استكشاف البيانات وفهم أنماط مغادرة العملاء",
        "total":         "إجمالي العملاء",
        "churned":       "غادروا",
        "retained":      "بقوا",
        "avg_age":       "متوسط العمر",
        "avg_balance":   "متوسط الرصيد",
        "avg_credit":    "متوسط درجة الائتمان",
        "tab_geo":       "🌍 الجغرافيا",
        "tab_demo":      "👥 الديموغرافيا",
        "tab_fin":       "💰 المالية",
        "tab_corr":      "🔗 الارتباط",
        "tab_raw":       "🗃️ البيانات الخام",
        "churn_geo":     "عدد المغادرين حسب الدولة",
        "churn_rate_geo":"نسبة المغادرة % حسب الدولة",
        "age_dist":      "توزيع العمر حسب المغادرة",
        "gender_churn":  "المغادرة حسب الجنس",
        "products_churn":"المغادرة حسب عدد المنتجات",
        "active_churn":  "العضوية النشطة والمغادرة",
        "balance_dist":  "توزيع الرصيد حسب المغادرة",
        "credit_dist":   "درجة الائتمان حسب المغادرة",
        "salary_dist":   "الراتب المتوقع حسب المغادرة",
        "tenure_churn":  "سنوات العضوية حسب المغادرة",
        "corr_title":    "خريطة الارتباط",
        "corr_sub":      "ارتباط الميزات العددية مع المغادرة",
        "raw_title":     "البيانات الخام",
        "shape":         "الشكل",
        "stayed":        "بقي",
        "churned_lbl":   "غادر",
        "churn_insight": "رؤية رئيسية",
        "years":         "سنة",
    },
}
t = T[LANG]

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base, "data", "raw", "Churn_Modelling.csv")
    df = pd.read_csv(path)
    df = df.drop(["RowNumber", "CustomerId", "Surname"], axis=1)
    df["Exited_Label"] = df["Exited"].map({0: t["stayed"], 1: t["churned_lbl"]})
    return df

df = load_data()

churn_rate   = df["Exited"].mean() * 100
retain_rate  = 100 - churn_rate
n_churned    = df["Exited"].sum()
n_retained   = (df["Exited"] == 0).sum()

# ─── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem">
  <h1 style="font-family:Syne,sans-serif;font-weight:800;
             background:linear-gradient(135deg,#00d4ff,#7c3aed);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin-bottom:6px">{t["title"]}</h1>
  <p style="color:var(--text-muted,#64748b);font-size:0.9rem;margin:0">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, label, value, delta=None, delta_color="#10b981"):
    delta_html = f'<div style="font-size:0.72rem;color:{delta_color};margin-top:2px">{delta}</div>' if delta else ""
    col.markdown(f"""
    <div style="background:{'#111827' if THEME=='dark' else '#fff'};
                border:1px solid {'rgba(0,212,255,0.15)' if THEME=='dark' else 'rgba(3,105,161,0.18)'};
                border-radius:14px;padding:16px 14px;text-align:center;
                box-shadow:0 4px 20px rgba(0,0,0,0.3)">
      <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.12em;
                  text-transform:uppercase;color:{'#64748b' if THEME=='dark' else '#94a3b8'};
                  font-family:Syne,sans-serif;margin-bottom:6px">{label}</div>
      <div style="font-size:1.45rem;font-weight:800;font-family:Syne,sans-serif;
                  color:{'#f1f5f9' if THEME=='dark' else '#0f172a'}">{value}</div>
      {delta_html}
    </div>
    """, unsafe_allow_html=True)

kpi(k1, t["total"],       f"{len(df):,}")
kpi(k2, t["churned"],     f"{n_churned:,}",   f"▲ {churn_rate:.1f}%",  "#f43f5e")
kpi(k3, t["retained"],    f"{n_retained:,}",  f"▼ {retain_rate:.1f}%", "#10b981")
kpi(k4, t["avg_age"],     f"{df['Age'].mean():.0f} {t['years']}")
kpi(k5, t["avg_balance"],  f"${df['Balance'].mean():,.0f}")
kpi(k6, t["avg_credit"],   f"{df['CreditScore'].mean():.0f}")

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    t["tab_geo"], t["tab_demo"], t["tab_fin"], t["tab_corr"], t["tab_raw"]
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GEOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        geo_counts = df.groupby(["Geography","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(
            geo_counts, x="Geography", y="Count", color="Exited_Label",
            barmode="group", title=t["churn_geo"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        churn_geo = df.groupby("Geography")["Exited"].mean().reset_index()
        churn_geo["Rate"] = (churn_geo["Exited"] * 100).round(1)
        fig = px.bar(
            churn_geo, x="Geography", y="Rate",
            color="Rate", color_continuous_scale=["#10b981","#f59e0b","#f43f5e"],
            title=t["churn_rate_geo"], text="Rate",
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # Insight
    top_geo = churn_geo.loc[churn_geo["Rate"].idxmax(), "Geography"]
    top_rate = churn_geo["Rate"].max()
    st.markdown(f"""
    <div style="background:rgba(244,63,94,0.08);border-left:3px solid #f43f5e;
                border-radius:8px;padding:12px 16px;margin-top:8px;font-size:0.85rem">
        💡 <b style="color:#f43f5e">{t["churn_insight"]}:</b>
        <span style="color:{'#cbd5e1' if THEME=='dark' else '#334155'}">
        {top_geo} has the highest churn rate at <b>{top_rate:.1f}%</b>
        </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            df, x="Age", color="Exited_Label", nbins=30,
            barmode="overlay", opacity=0.75, title=t["age_dist"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        gender_churn = df.groupby(["Gender","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(
            gender_churn, x="Gender", y="Count", color="Exited_Label",
            barmode="group", title=t["gender_churn"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        prod_churn = df.groupby(["NumOfProducts","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(
            prod_churn, x="NumOfProducts", y="Count", color="Exited_Label",
            barmode="group", title=t["products_churn"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        active_churn = df.groupby(["IsActiveMember","Exited_Label"]).size().reset_index(name="Count")
        active_churn["IsActiveMember"] = active_churn["IsActiveMember"].map({0:"Inactive", 1:"Active"})
        fig = px.bar(
            active_churn, x="IsActiveMember", y="Count", color="Exited_Label",
            barmode="group", title=t["active_churn"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # Churn rate by age group
    st.markdown("---")
    df["AgeGroup"] = pd.cut(df["Age"], bins=[18,30,40,50,60,100],
                             labels=["18-30","31-40","41-50","51-60","60+"])
    age_churn = df.groupby("AgeGroup", observed=True)["Exited"].mean().reset_index()
    age_churn["Rate"] = (age_churn["Exited"] * 100).round(1)
    fig = px.line(
        age_churn, x="AgeGroup", y="Rate", markers=True,
        title="Churn Rate % by Age Group",
        color_discrete_sequence=[C["churned"]],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=9))
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FINANCIAL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns(2)

    with c1:
        fig = px.violin(
            df, x="Exited_Label", y="Balance", color="Exited_Label",
            box=True, title=t["balance_dist"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.violin(
            df, x="Exited_Label", y="CreditScore", color="Exited_Label",
            box=True, title=t["credit_dist"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig = px.violin(
            df, x="Exited_Label", y="EstimatedSalary", color="Exited_Label",
            box=True, title=t["salary_dist"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        tenure_churn = df.groupby(["Tenure","Exited_Label"]).size().reset_index(name="Count")
        fig = px.line(
            tenure_churn, x="Tenure", y="Count", color="Exited_Label",
            markers=True, title=t["tenure_churn"],
            color_discrete_map={t["stayed"]: C["stayed"], t["churned_lbl"]: C["churned"]},
        )
        fig.update_traces(line=dict(width=2.5))
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # Financial summary table
    st.markdown("---")
    fin_summary = df.groupby("Exited_Label")[["Balance","CreditScore","EstimatedSalary"]].mean().round(1)
    fin_summary.columns = ["Avg Balance ($)", "Avg Credit Score", "Avg Salary ($)"]
    st.dataframe(
        fin_summary.style.format("{:,.1f}").background_gradient(cmap="Blues", axis=0),
        use_container_width=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"<p style='color:{'#94a3b8' if THEME=='dark' else '#475569'};font-size:0.85rem'>{t['corr_sub']}</p>", unsafe_allow_html=True)

    num_df  = df.select_dtypes(include="number")
    corr    = num_df.corr().round(2)

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdBu_r",
        zmid=0,
        text=corr.values,
        texttemplate="%{text:.2f}",
        textfont=dict(size=10),
        hoverongaps=False,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=t["corr_title"],
        height=520,
    )
    fig.update_xaxes(tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    # Top correlations with Exited
    corr_exited = corr["Exited"].drop("Exited").abs().sort_values(ascending=False)
    top5 = corr_exited.head(5).reset_index()
    top5.columns = ["Feature", "|Correlation with Churn|"]
    st.dataframe(top5, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — RAW DATA
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown(f"### {t['raw_title']}")

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        geo_filter = st.multiselect("Geography", df["Geography"].unique(), default=df["Geography"].unique())
    with fc2:
        gen_filter = st.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
    with fc3:
        exit_filter = st.multiselect("Exited", [0, 1], default=[0, 1])

    filtered = df[
        df["Geography"].isin(geo_filter) &
        df["Gender"].isin(gen_filter) &
        df["Exited"].isin(exit_filter)
    ].drop("Exited_Label", axis=1)

    st.dataframe(filtered, use_container_width=True, height=420)
    st.caption(f"{t['shape']}: {filtered.shape[0]:,} rows × {filtered.shape[1]} cols")

    # Download
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "filtered_data.csv", "text/csv")
