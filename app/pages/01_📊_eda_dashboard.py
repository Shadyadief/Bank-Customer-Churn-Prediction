import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="EDA Dashboard | Bank Churn",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from spider import spider
spider()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

THEME = st.session_state.get("theme", "dark")
LANG  = st.session_state.get("lang",  "en")

# ── Palette ────────────────────────────────────────────────────────────────────
if THEME == "dark":
    STAYED   = "#00d4ff"
    CHURNED  = "#f43f5e"
    GRID     = "#1e293b"
    TEXT_C   = "#94a3b8"
    TEXT_H   = "#f1f5f9"
    TEXT_SUB = "#cbd5e1"
    CARD_BG  = "#111827"
    CARD_BDR = "rgba(0,212,255,0.15)"
    INS_BG   = "rgba(244,63,94,0.08)"
    INS_OK   = "rgba(16,185,129,0.08)"
else:
    STAYED   = "#0369a1"
    CHURNED  = "#e11d48"
    GRID     = "#e2e8f0"
    TEXT_C   = "#475569"
    TEXT_H   = "#0f172a"
    TEXT_SUB = "#334155"
    CARD_BG  = "#ffffff"
    CARD_BDR = "rgba(3,105,161,0.18)"
    INS_BG   = "rgba(225,29,72,0.07)"
    INS_OK   = "rgba(5,150,105,0.07)"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font        =dict(family="DM Mono, monospace", color=TEXT_C, size=12),
    title_font  =dict(family="Syne, sans-serif",   color=TEXT_H, size=15),
    xaxis       =dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=TEXT_C)),
    yaxis       =dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(color=TEXT_C)),
    legend      =dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_C)),
    margin      =dict(l=20, r=20, t=50, b=20),
)

T = {
    "en": {
        "title":"📊 EDA Dashboard","subtitle":"Exploratory Data Analysis — Understanding Churn Patterns",
        "total":"Total Customers","churned":"Churned","retained":"Retained",
        "avg_age":"Avg Age","avg_balance":"Avg Balance","avg_credit":"Avg Credit Score",
        "tab_geo":"🌍 Geography","tab_demo":"👥 Demographics","tab_fin":"💰 Financial",
        "tab_corr":"🔗 Correlation","tab_raw":"🗃️ Raw Data",
        "churn_geo":"Churn Count by Geography","churn_rate_geo":"Churn Rate % by Geography",
        "age_dist":"Age Distribution by Churn","gender_churn":"Churn by Gender",
        "products_churn":"Churn by Number of Products","active_churn":"Active Member vs Churn",
        "balance_dist":"Balance Distribution by Churn","credit_dist":"Credit Score Distribution",
        "salary_dist":"Estimated Salary by Churn","tenure_churn":"Tenure (Years) by Churn",
        "corr_title":"Correlation Heatmap","corr_sub":"Numeric feature correlations with Churn",
        "raw_title":"Raw Dataset","shape":"Shape",
        "stayed":"Stayed","churned_lbl":"Churned","churn_insight":"Key Insight","years":"years",
        "age_group_title":"Churn Rate % by Age Group",
        "fin_table":"Financial Summary by Churn Status",
        "top_corr":"Top Features Correlated with Churn",
        "download":"⬇️ Download CSV",
    },
    "ar": {
        "title":"📊 لوحة التحليل الاستكشافي","subtitle":"استكشاف البيانات وفهم أنماط مغادرة العملاء",
        "total":"إجمالي العملاء","churned":"غادروا","retained":"بقوا",
        "avg_age":"متوسط العمر","avg_balance":"متوسط الرصيد","avg_credit":"متوسط درجة الائتمان",
        "tab_geo":"🌍 الجغرافيا","tab_demo":"👥 الديموغرافيا","tab_fin":"💰 المالية",
        "tab_corr":"🔗 الارتباط","tab_raw":"🗃️ البيانات الخام",
        "churn_geo":"عدد المغادرين حسب الدولة","churn_rate_geo":"نسبة المغادرة % حسب الدولة",
        "age_dist":"توزيع العمر حسب المغادرة","gender_churn":"المغادرة حسب الجنس",
        "products_churn":"المغادرة حسب عدد المنتجات","active_churn":"العضوية النشطة والمغادرة",
        "balance_dist":"توزيع الرصيد حسب المغادرة","credit_dist":"درجة الائتمان حسب المغادرة",
        "salary_dist":"الراتب المتوقع حسب المغادرة","tenure_churn":"سنوات العضوية حسب المغادرة",
        "corr_title":"خريطة الارتباط","corr_sub":"ارتباط الميزات العددية مع المغادرة",
        "raw_title":"البيانات الخام","shape":"الشكل",
        "stayed":"بقي","churned_lbl":"غادر","churn_insight":"رؤية رئيسية","years":"سنة",
        "age_group_title":"نسبة المغادرة % حسب الفئة العمرية",
        "fin_table":"ملخص مالي حسب حالة المغادرة",
        "top_corr":"أعلى الميزات ارتباطاً بالمغادرة",
        "download":"⬇️ تحميل CSV",
    },
}
t = T[LANG]

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(stayed_lbl, churned_lbl):
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base, "data", "raw", "Churn_Modelling.csv")
    df = pd.read_csv(path)
    df = df.drop(["RowNumber", "CustomerId", "Surname"], axis=1)
    df["Exited_Label"] = df["Exited"].map({0: stayed_lbl, 1: churned_lbl})
    return df

df = load_data(t["stayed"], t["churned_lbl"])
churn_rate  = df["Exited"].mean() * 100
retain_rate = 100 - churn_rate
n_churned   = int(df["Exited"].sum())
n_retained  = int((df["Exited"] == 0).sum())

COLOR_MAP = {t["stayed"]: STAYED, t["churned_lbl"]: CHURNED}

# ── Component CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
[data-testid="stHorizontalBlock"] {{ align-items: stretch !important; }}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
    display: flex !important; flex-direction: column !important;
}}
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BDR};
    border-radius: 16px; padding: 18px 12px;
    text-align: center; height: 100%;
    min-height: 100px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    transition: transform .22s ease, box-shadow .22s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.18);
}}
.kpi-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 14px 36px rgba(0,0,0,.28);
}}
.kpi-label {{
    font-size: .66rem; font-weight: 700; letter-spacing: .13em;
    text-transform: uppercase; color: {TEXT_C};
    font-family: Syne,sans-serif; margin-bottom: 7px;
}}
.kpi-value {{
    font-size: 1.5rem; font-weight: 800;
    font-family: Syne,sans-serif; color: {TEXT_H};
    line-height: 1;
}}
.kpi-delta {{ font-size: .72rem; margin-top: 4px; font-weight: 600; }}

.chart-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BDR};
    border-radius: 16px; padding: 4px 4px 0;
    height: 100%;
    transition: transform .22s ease, box-shadow .22s ease;
}}
.chart-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 14px 36px rgba(0,0,0,.22);
}}

.insight-box {{
    border-radius: 10px; padding: 13px 16px;
    margin-top: 12px; font-size: .85rem;
    display: flex; align-items: flex-start; gap: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ── Page Header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:1.8rem">
  <h1 style="font-family:Syne,sans-serif;font-weight:800;font-size:clamp(1.6rem,3vw,2.4rem);
             background:linear-gradient(135deg,#00d4ff,#7c3aed);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin-bottom:5px;line-height:1.2">{t["title"]}</h1>
  <p style="color:{TEXT_C};font-size:.9rem;margin:0">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
KPI_DATA = [
    (k1, t["total"],      f"{len(df):,}",              None,                    "#00d4ff"),
    (k2, t["churned"],    f"{n_churned:,}",             f"▲ {churn_rate:.1f}%", "#f43f5e"),
    (k3, t["retained"],   f"{n_retained:,}",            f"▼ {retain_rate:.1f}%","#10b981"),
    (k4, t["avg_age"],    f"{df['Age'].mean():.0f} {t['years']}", None,         "#7c3aed"),
    (k5, t["avg_balance"],f"${df['Balance'].mean():,.0f}", None,                "#f59e0b"),
    (k6, t["avg_credit"], f"{df['CreditScore'].mean():.0f}", None,              "#3b82f6"),
]
for col, label, value, delta, color in KPI_DATA:
    delta_html = f'<div class="kpi-delta" style="color:{color}">{delta}</div>' if delta else ""
    col.markdown(f"""
    <div class="kpi-card" style="border-top:3px solid {color}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value" style="color:{color}">{value}</div>
      {delta_html}
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.6rem'></div>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    t["tab_geo"], t["tab_demo"], t["tab_fin"], t["tab_corr"], t["tab_raw"]
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GEOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        geo_counts = df.groupby(["Geography","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(geo_counts, x="Geography", y="Count", color="Exited_Label",
                     barmode="group", title=t["churn_geo"], color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        churn_geo = df.groupby("Geography")["Exited"].mean().reset_index()
        churn_geo["Rate"] = (churn_geo["Exited"] * 100).round(1)
        fig = px.bar(churn_geo, x="Geography", y="Rate",
                     color="Rate", color_continuous_scale=["#10b981","#f59e0b","#f43f5e"],
                     title=t["churn_rate_geo"], text="Rate")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    top_geo  = churn_geo.loc[churn_geo["Rate"].idxmax(), "Geography"]
    top_rate = churn_geo["Rate"].max()
    low_geo  = churn_geo.loc[churn_geo["Rate"].idxmin(), "Geography"]
    low_rate = churn_geo["Rate"].min()
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-top:10px">
      <div class="insight-box" style="background:{INS_BG};border-left:3px solid #f43f5e;flex:1">
        💡 <span><b style="color:#f43f5e">{t["churn_insight"]}:</b>
        <span style="color:{TEXT_SUB}"> {top_geo} — highest churn at <b>{top_rate:.1f}%</b></span></span>
      </div>
      <div class="insight-box" style="background:{INS_OK};border-left:3px solid #10b981;flex:1">
        ✅ <span><b style="color:#10b981">Best Retention:</b>
        <span style="color:{TEXT_SUB}"> {low_geo} — lowest churn at <b>{low_rate:.1f}%</b></span></span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = px.histogram(df, x="Age", color="Exited_Label", nbins=30,
                           barmode="overlay", opacity=0.75, title=t["age_dist"],
                           color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        gender_churn = df.groupby(["Gender","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(gender_churn, x="Gender", y="Count", color="Exited_Label",
                     barmode="group", title=t["gender_churn"], color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        prod_churn = df.groupby(["NumOfProducts","Exited_Label"]).size().reset_index(name="Count")
        fig = px.bar(prod_churn, x="NumOfProducts", y="Count", color="Exited_Label",
                     barmode="group", title=t["products_churn"], color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        active_churn = df.groupby(["IsActiveMember","Exited_Label"]).size().reset_index(name="Count")
        active_churn["IsActiveMember"] = active_churn["IsActiveMember"].map({0:"Inactive",1:"Active"})
        fig = px.bar(active_churn, x="IsActiveMember", y="Count", color="Exited_Label",
                     barmode="group", title=t["active_churn"], color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    df["AgeGroup"] = pd.cut(df["Age"], bins=[18,30,40,50,60,100],
                             labels=["18-30","31-40","41-50","51-60","60+"])
    age_churn = df.groupby("AgeGroup", observed=True)["Exited"].mean().reset_index()
    age_churn["Rate"] = (age_churn["Exited"] * 100).round(1)
    fig = px.area(age_churn, x="AgeGroup", y="Rate", markers=True,
                  title=t["age_group_title"],
                  color_discrete_sequence=[CHURNED])
    fig.update_traces(line=dict(width=3), marker=dict(size=9),
                      fill="tozeroy",
                      fillcolor=f"rgba(244,63,94,0.12)" if THEME=="dark" else "rgba(225,29,72,0.08)")
    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Insight
    peak_age = age_churn.loc[age_churn["Rate"].idxmax(), "AgeGroup"]
    peak_rate = age_churn["Rate"].max()
    st.markdown(f"""
    <div class="insight-box" style="background:{INS_BG};border-left:3px solid #f43f5e;margin-top:8px">
      💡 <span><b style="color:#f43f5e">{t["churn_insight"]}:</b>
      <span style="color:{TEXT_SUB}"> Age group <b>{peak_age}</b> has the highest churn at <b>{peak_rate:.1f}%</b></span></span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — FINANCIAL
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns(2)
    for col, y_col, title in [
        (c1, "Balance",         t["balance_dist"]),
        (c2, "CreditScore",     t["credit_dist"]),
    ]:
        with col:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            fig = px.violin(df, x="Exited_Label", y=y_col, color="Exited_Label",
                            box=True, title=title, color_discrete_map=COLOR_MAP)
            fig.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = px.violin(df, x="Exited_Label", y="EstimatedSalary", color="Exited_Label",
                        box=True, title=t["salary_dist"], color_discrete_map=COLOR_MAP)
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        tenure_churn = df.groupby(["Tenure","Exited_Label"]).size().reset_index(name="Count")
        fig = px.line(tenure_churn, x="Tenure", y="Count", color="Exited_Label",
                      markers=True, title=t["tenure_churn"], color_discrete_map=COLOR_MAP)
        fig.update_traces(line=dict(width=2.5))
        fig.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h4 style='font-family:Syne,sans-serif;color:{TEXT_H};margin:1.4rem 0 .6rem'>{t['fin_table']}</h4>",
                unsafe_allow_html=True)
    fin_summary = df.groupby("Exited_Label")[["Balance","CreditScore","EstimatedSalary"]].mean().round(1)
    fin_summary.columns = ["Avg Balance ($)", "Avg Credit Score", "Avg Salary ($)"]
    st.dataframe(fin_summary.style.format("{:,.1f}").background_gradient(cmap="Blues", axis=0),
                 use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"<p style='color:{TEXT_C};font-size:.85rem;margin-bottom:1rem'>{t['corr_sub']}</p>",
                unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        num_df = df.select_dtypes(include="number")
        corr   = num_df.corr().round(2)
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
            colorscale="RdBu_r", zmid=0,
            text=corr.values, texttemplate="%{text:.2f}",
            textfont=dict(size=10), hoverongaps=False,
        ))
        fig.update_layout(**PLOTLY_LAYOUT, title=t["corr_title"], height=480)
        fig.update_xaxes(tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown(f"<h4 style='font-family:Syne,sans-serif;color:{TEXT_H};margin-bottom:.8rem'>{t['top_corr']}</h4>",
                    unsafe_allow_html=True)
        corr_exited = corr["Exited"].drop("Exited").abs().sort_values(ascending=False)
        for i, (feat, val) in enumerate(corr_exited.head(6).items()):
            bar_color = CHURNED if val > 0.1 else STAYED
            pct = int(val * 100 / corr_exited.max())
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;
                          font-size:.78rem;color:{TEXT_H};margin-bottom:4px">
                <span style="font-weight:600">{feat}</span>
                <span style="color:{bar_color};font-weight:700">{val:.3f}</span>
              </div>
              <div style="background:{GRID};border-radius:99px;height:6px">
                <div style="width:{pct}%;background:{bar_color};
                            border-radius:99px;height:6px;
                            transition:width .6s ease"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — RAW DATA
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown(f"<h3 style='font-family:Syne,sans-serif;color:{TEXT_H};margin-bottom:1rem'>{t['raw_title']}</h3>",
                unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        geo_filter  = st.multiselect("Geography", df["Geography"].unique(), default=list(df["Geography"].unique()))
    with fc2:
        gen_filter  = st.multiselect("Gender",    df["Gender"].unique(),    default=list(df["Gender"].unique()))
    with fc3:
        exit_filter = st.multiselect("Exited",    [0, 1],                  default=[0, 1])

    filtered = df[
        df["Geography"].isin(geo_filter) &
        df["Gender"].isin(gen_filter) &
        df["Exited"].isin(exit_filter)
    ].drop("Exited_Label", axis=1)

    st.dataframe(filtered, use_container_width=True, height=420)

    col_info, col_dl = st.columns([3, 1])
    with col_info:
        st.caption(f"{t['shape']}: {filtered.shape[0]:,} rows × {filtered.shape[1]} cols")
    with col_dl:
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(t["download"], csv, "filtered_data.csv", "text/csv",
                           use_container_width=True)
