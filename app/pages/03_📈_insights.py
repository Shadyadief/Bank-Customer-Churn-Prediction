import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ⚡⚡⚡ PAGE CONFIG - أول حاجة ⚡⚡⚡
st.set_page_config(
    page_title="EDA Dashboard | Bank Churn",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",  # مهم جداً
)

# ⚡⚡⚡ استدعاء spider واستقبال القيم ⚡⚡⚡
from spider import spider
theme, lang = spider()  # ✅ استقبل القيم اللي spider بترجعها

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ─── Session State ─────────────────────────────────────────────────────────────
THEME = st.session_state.get("theme", "dark")
LANG  = st.session_state.get("lang",  "en")

# ─── Theme Colors ──────────────────────────────────────────────────────────────
C = {
    "dark": {
        "bg":       "#111827", "bg2": "#0f172a",
        "border":   "rgba(0,212,255,0.15)",
        "text":     "#94a3b8", "text_h": "#f1f5f9", "text_sub": "#cbd5e1",
        "grid":     "#1e293b",
        "ins_age":  ("rgba(245,158,11,0.10)",  "#f59e0b"),
        "ins_prod": ("rgba(244,63,94,0.10)",   "#f43f5e"),
        "ins_act":  ("rgba(16,185,129,0.10)",  "#10b981"),
        "ins_ger":  ("rgba(59,130,246,0.10)",  "#3b82f6"),
        "ins_bal":  ("rgba(124,58,237,0.10)",  "#7c3aed"),
        "ins_gen":  ("rgba(0,212,255,0.10)",   "#00d4ff"),
    },
    "light": {
        "bg":       "#ffffff", "bg2": "#f0f6ff",
        "border":   "rgba(3,105,161,0.18)",
        "text":     "#475569", "text_h": "#0f172a", "text_sub": "#334155",
        "grid":     "#e2e8f0",
        "ins_age":  ("rgba(245,158,11,0.08)",  "#d97706"),
        "ins_prod": ("rgba(244,63,94,0.08)",   "#e11d48"),
        "ins_act":  ("rgba(16,185,129,0.08)",  "#059669"),
        "ins_ger":  ("rgba(59,130,246,0.08)",  "#2563eb"),
        "ins_bal":  ("rgba(124,58,237,0.08)",  "#6d28d9"),
        "ins_gen":  ("rgba(0,212,255,0.08)",   "#0369a1"),
    },
}[THEME]

PLOTLY_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = dict(family="DM Mono, monospace", color=C["text"], size=12),
    title_font    = dict(family="Syne, sans-serif",   color=C["text_h"], size=15),
    xaxis         = dict(gridcolor=C["grid"], linecolor=C["grid"], tickfont=dict(color=C["text"])),
    yaxis         = dict(gridcolor=C["grid"], linecolor=C["grid"], tickfont=dict(color=C["text"])),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["text"])),
    margin        = dict(l=20, r=20, t=50, b=20),
)

# ─── Translations ──────────────────────────────────────────────────────────────
T = {
    "en": {
        "title":        "📈 Model Insights",
        "subtitle":     "Model comparison, feature importance & key churn drivers",
        "model_warn":   "⚠️ Model files not found! Run training first.",
        "best_model":   "🏆 Best Model",
        "tab_compare":  "🤖 Model Comparison",
        "tab_feat":     "🔍 Feature Importance",
        "tab_insights": "💡 Key Insights",
        "tab_radar":    "🕸️ Radar Analysis",
        "compare_sub":  "Performance metrics across all trained models",
        "acc_chart":    "Accuracy Comparison",
        "auc_chart":    "ROC-AUC Comparison",
        "f1_chart":     "F1-Score (Churn Class)",
        "full_table":   "📊 Full Metrics Table",
        "feat_title":   "Feature Importance — XGBoost",
        "feat_sub":     "Higher value = more influence on churn prediction",
        "top_feat":     "Top Feature",
        "insights_title": "Key Churn Drivers",
        "insights": [
            ("👴", "Age 45–60", "ins_age",
             "Customers aged 45–60 have the highest churn rate. The bank needs tailored products for this segment."),
            ("📦", "3–4 Products", "ins_prod",
             "Customers with 3–4 products churn at a surprisingly high rate — a counter-intuitive pattern worth investigating."),
            ("✅", "Active Membership", "ins_act",
             "Active members churn significantly less. Boosting engagement directly reduces churn."),
            ("🇩🇪", "Germany ~32%", "ins_ger",
             "Germany customers churn at ~32% vs France & Spain — requires a dedicated retention strategy."),
            ("💰", "Zero Balance", "ins_bal",
             "Zero-balance customers churn less — likely using accounts for daily transactions."),
            ("👩", "Female Customers", "ins_gen",
             "Female customers show a slightly higher churn tendency — worth exploring with targeted offers."),
        ],
        "radar_title":  "Model Performance Radar",
        "radar_sub":    "Multi-metric comparison across models",
        "metric_best":  "Best",
    },
    "ar": {
        "title":        "📈 رؤى الموديل",
        "subtitle":     "مقارنة الموديلات وأهمية الميزات وأبرز عوامل المغادرة",
        "model_warn":   "⚠️ ملفات الموديل غير موجودة! قم بتشغيل التدريب أولاً.",
        "best_model":   "🏆 أفضل موديل",
        "tab_compare":  "🤖 مقارنة الموديلات",
        "tab_feat":     "🔍 أهمية الميزات",
        "tab_insights": "💡 الرؤى الرئيسية",
        "tab_radar":    "🕸️ تحليل الرادار",
        "compare_sub":  "مقاييس الأداء لجميع الموديلات المدربة",
        "acc_chart":    "مقارنة الدقة",
        "auc_chart":    "مقارنة ROC-AUC",
        "f1_chart":     "F1-Score (فئة المغادرة)",
        "full_table":   "📊 جدول المقارنة الكامل",
        "feat_title":   "أهمية الميزات — XGBoost",
        "feat_sub":     "القيمة الأعلى = تأثير أكبر على توقع المغادرة",
        "top_feat":     "أهم ميزة",
        "insights_title": "أبرز عوامل المغادرة",
        "insights": [
            ("👴", "العمر 45–60", "ins_age",
             "العملاء بين 45–60 سنة لديهم أعلى نسبة مغادرة. البنك يحتاج منتجات مخصصة لهذه الفئة."),
            ("📦", "3–4 منتجات", "ins_prod",
             "العملاء الذين لديهم 3–4 منتجات يغادرون بنسبة مرتفعة بشكل مفاجئ — ظاهرة تستحق التحقيق."),
            ("✅", "العضوية النشطة", "ins_act",
             "الأعضاء النشطون يغادرون بنسبة أقل بكثير. زيادة التفاعل تقلل المغادرة مباشرة."),
            ("🇩🇪", "ألمانيا ~32%", "ins_ger",
             "عملاء ألمانيا يغادرون بنسبة ~32% مقارنة بفرنسا وإسبانيا — يحتاج استراتيجية احتفاظ خاصة."),
            ("💰", "الرصيد الصفري", "ins_bal",
             "العملاء ذوو الرصيد الصفري يغادرون بنسبة أقل — غالباً يستخدمون حساباتهم للمعاملات اليومية."),
            ("👩", "العميلات", "ins_gen",
             "العميلات لديهن ميل أعلى قليلاً للمغادرة — يستحق الاستكشاف بعروض موجهة."),
        ],
        "radar_title":  "رادار أداء الموديلات",
        "radar_sub":    "مقارنة متعددة الأبعاد بين الموديلات",
        "metric_best":  "الأفضل",
    },
}
t = T[LANG]

# ─── Load Metrics ──────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_metrics():
    try:
        metrics  = joblib.load(os.path.join(_BASE, "models", "model_metrics.pkl"))
        feat_imp = joblib.load(os.path.join(_BASE, "models", "feature_importance.pkl"))
        return pd.DataFrame(metrics), feat_imp, True
    except Exception:
        fallback_metrics = [
            {"Model": "Logistic Regression", "Accuracy": 0.8115, "ROC-AUC": 0.7634, "F1-Score (Churn)": 0.5012, "Precision": 0.5823, "Recall": 0.4401},
            {"Model": "Random Forest",        "Accuracy": 0.8670, "ROC-AUC": 0.8571, "F1-Score (Churn)": 0.6089, "Precision": 0.7142, "Recall": 0.5312},
            {"Model": "XGBoost",              "Accuracy": 0.8720, "ROC-AUC": 0.8812, "F1-Score (Churn)": 0.6241, "Precision": 0.7301, "Recall": 0.5450},
        ]
        fallback_feat = {
            "Age":               0.2341,
            "NumOfProducts":     0.1892,
            "IsActiveMember":    0.1654,
            "Balance":           0.1423,
            "Geography_Germany": 0.0891,
            "CreditScore":       0.0712,
            "Gender_Male":       0.0534,
            "Tenure":            0.0421,
            "EstimatedSalary":   0.0389,
            "HasCrCard":         0.0312,
            "Geography_Spain":   0.0231,
        }
        return pd.DataFrame(fallback_metrics), fallback_feat, False

df_models, feat_importance, loaded = load_metrics()

if not loaded:
    st.info("📊 Showing sample data — run train_model.py to load real results.")

# ─── Derived Info ──────────────────────────────────────────────────────────────
metric_cols   = [c for c in df_models.columns if c != "Model"]
best_model_row = df_models.loc[df_models["Accuracy"].idxmax()]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-bottom:1.5rem">
  <h1 style="font-family:Syne,sans-serif;font-weight:800;
             background:linear-gradient(135deg,#10b981,#00d4ff);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin-bottom:6px">{t["title"]}</h1>
  <p style="color:{C['text']};font-size:0.9rem;margin:0">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ─── Best Model Banner ─────────────────────────────────────────────────────────
cols_kpi = st.columns(len(metric_cols) + 1)

# Best model badge
cols_kpi[0].markdown(f"""
<div style="background:linear-gradient(135deg,rgba(16,185,129,0.15),rgba(0,212,255,0.10));
            border:1px solid rgba(16,185,129,0.35);border-radius:14px;
            padding:16px 14px;text-align:center;height:100%">
  <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.12em;
              text-transform:uppercase;color:#10b981;font-family:Syne,sans-serif;
              margin-bottom:6px">{t["best_model"]}</div>
  <div style="font-size:1.15rem;font-weight:800;font-family:Syne,sans-serif;
              color:{C['text_h']}">{best_model_row['Model']}</div>
</div>
""", unsafe_allow_html=True)

# Metric KPIs
METRIC_COLORS = {"Accuracy": "#00d4ff", "ROC-AUC": "#7c3aed",
                 "F1-Score (Churn)": "#10b981", "Precision": "#f59e0b",
                 "Recall": "#f43f5e"}
for i, mc in enumerate(metric_cols):
    val   = best_model_row[mc]
    color = METRIC_COLORS.get(mc, "#00d4ff")
    cols_kpi[i+1].markdown(f"""
    <div style="background:{C['bg']};border:1px solid {C['border']};
                border-top:3px solid {color};border-radius:14px;
                padding:16px 14px;text-align:center">
      <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
                  text-transform:uppercase;color:{C['text']};font-family:Syne,sans-serif;
                  margin-bottom:6px">{mc}</div>
      <div style="font-size:1.4rem;font-weight:800;font-family:Syne,sans-serif;
                  color:{color}">{val:.3f}</div>
      <div style="font-size:0.65rem;color:{C['text']};margin-top:2px">
        {t["metric_best"]} ✓
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    t["tab_compare"], t["tab_feat"], t["tab_insights"], t["tab_radar"]
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MODEL COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"<p style='color:{C['text']};font-size:0.85rem;margin-bottom:1.2rem'>{t['compare_sub']}</p>",
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    def metric_bar(col, metric, title, color_scale, y_range):
        fig = px.bar(
            df_models, x="Model", y=metric,
            color=metric, color_continuous_scale=color_scale,
            title=title, text=metric,
        )
        fig.update_traces(
            texttemplate="%{text:.3f}",
            textposition="outside",
            marker_line_width=0,
        )
        fig.update_layout(
            **PLOTLY_LAYOUT,
            coloraxis_showscale=False,
            yaxis_range=y_range,
        )
        col.plotly_chart(fig, use_container_width=True)

    metric_bar(c1, "Accuracy",        t["acc_chart"], ["#0f172a","#00d4ff"], [0.70, 0.95])
    metric_bar(c2, "ROC-AUC",         t["auc_chart"], ["#0f172a","#7c3aed"], [0.60, 0.95])
    metric_bar(c3, "F1-Score (Churn)",t["f1_chart"],  ["#0f172a","#10b981"], [0.40, 0.80])

    # Full table
    st.markdown(f"### {t['full_table']}")

    def highlight_max(s):
        is_max = s == s.max()
        return [f"color: #10b981; font-weight: 700" if v else "" for v in is_max]

    styled = (
        df_models.style
        .apply(highlight_max, subset=metric_cols)
        .format({c: "{:.4f}" for c in metric_cols})
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FEATURE IMPORTANCE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"<p style='color:{C['text']};font-size:0.85rem;margin-bottom:1rem'>{t['feat_sub']}</p>",
                unsafe_allow_html=True)

    df_feat = pd.DataFrame({
        "Feature":    list(feat_importance.keys()),
        "Importance": list(feat_importance.values()),
    }).sort_values("Importance", ascending=True)

    top_feat  = df_feat.iloc[-1]["Feature"]
    top_score = df_feat.iloc[-1]["Importance"]

    # Colour by importance rank
    n = len(df_feat)
    colors = []
    for i in range(n):
        frac = i / (n - 1) if n > 1 else 1
        if frac > 0.75:   colors.append("#f43f5e")
        elif frac > 0.50: colors.append("#f59e0b")
        elif frac > 0.25: colors.append("#00d4ff")
        else:             colors.append("#334155")

    fig = go.Figure(go.Bar(
        x=df_feat["Importance"],
        y=df_feat["Feature"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=df_feat["Importance"].round(4),
        textposition="outside",
        textfont=dict(color=C["text"], size=10),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=t["feat_title"],
        height=480,
    )
    fig.update_xaxes(title_text="Importance Score")
    st.plotly_chart(fig, use_container_width=True)

    # Top feature callout
    st.markdown(f"""
    <div style="background:rgba(244,63,94,0.10);border-left:3px solid #f43f5e;
                border-radius:8px;padding:12px 16px;font-size:0.85rem">
      🏅 <b style="color:#f43f5e">{t['top_feat']}:</b>
      <span style="color:{C['text_sub']}">
        <b style="color:{C['text_h']}">{top_feat}</b>
        — importance score <b>{top_score:.4f}</b>
      </span>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — KEY INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(f"""
    <h3 style="font-family:Syne,sans-serif;color:{C['text_h']};margin-bottom:1.2rem">
      {t["insights_title"]}
    </h3>
    """, unsafe_allow_html=True)

    insights = t["insights"]

    # Row 1: 3 cards
    row1 = st.columns(3)
    for i, (icon, title, color_key, desc) in enumerate(insights[:3]):
        bg, border = C[color_key]
        row1[i].markdown(f"""
        <div style="background:{bg};border:1px solid {border};
                    border-top:3px solid {border};border-radius:14px;
                    padding:22px 20px;height:100%;min-height:160px">
          <div style="font-size:2rem;margin-bottom:10px">{icon}</div>
          <div style="font-family:Syne,sans-serif;font-weight:700;
                      font-size:1rem;color:{C['text_h']};margin-bottom:8px">
            {title}
          </div>
          <div style="font-size:0.83rem;color:{C['text_sub']};line-height:1.6">
            {desc}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)

    # Row 2: 3 cards
    row2 = st.columns(3)
    for i, (icon, title, color_key, desc) in enumerate(insights[3:]):
        bg, border = C[color_key]
        row2[i].markdown(f"""
        <div style="background:{bg};border:1px solid {border};
                    border-top:3px solid {border};border-radius:14px;
                    padding:22px 20px;height:100%;min-height:160px">
          <div style="font-size:2rem;margin-bottom:10px">{icon}</div>
          <div style="font-family:Syne,sans-serif;font-weight:700;
                      font-size:1rem;color:{C['text_h']};margin-bottom:8px">
            {title}
          </div>
          <div style="font-size:0.83rem;color:{C['text_sub']};line-height:1.6">
            {desc}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Action recommendations
    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)

    actions_en = [
        "📧 Launch targeted retention campaigns for age 45–60",
        "🎁 Create bundled product offers to prevent over-saturation",
        "📱 Build an engagement app feature to boost active membership",
        "🇩🇪 Deploy a Germany-specific loyalty & retention program",
    ]
    actions_ar = [
        "📧 إطلاق حملات احتفاظ مستهدفة للفئة العمرية 45–60",
        "🎁 إنشاء عروض مجمعة للمنتجات لمنع التشبع",
        "📱 بناء ميزة تفاعل لزيادة نسبة الأعضاء النشطين",
        "🇩🇪 تطوير برنامج ولاء خاص بعملاء ألمانيا",
    ]
    actions      = actions_en if LANG == "en" else actions_ar
    action_title = "Recommended Actions" if LANG == "en" else "الإجراءات الموصى بها"

    actions_html = "".join([
        f'<div style="background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.12);'
        f'border-radius:10px;padding:12px 16px;font-size:0.82rem;color:{C["text_sub"]}">{a}</div>'
        for a in actions
    ])

    st.markdown(
        f'<div style="background:{C["bg"]};border:1px solid {C["border"]};'
        f'border-radius:16px;padding:24px 28px">'
        f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1.05rem;'
        f'color:{C["text_h"]};margin-bottom:16px">🎯 {action_title}</div>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">{actions_html}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RADAR CHART
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"<p style='color:{C['text']};font-size:0.85rem;margin-bottom:1rem'>{t['radar_sub']}</p>",
                unsafe_allow_html=True)

    radar_metrics = [c for c in metric_cols if c in df_models.columns]
    MODEL_COLORS  = ["#00d4ff", "#f43f5e", "#10b981", "#f59e0b", "#7c3aed"]
    FILL_COLORS   = ["rgba(0,212,255,0.10)", "rgba(244,63,94,0.10)", "rgba(16,185,129,0.10)", "rgba(245,158,11,0.10)", "rgba(124,58,237,0.10)"]

    fig = go.Figure()
    for i, row in df_models.iterrows():
        vals   = [row[m] for m in radar_metrics]
        vals  += [vals[0]]
        labels = radar_metrics + [radar_metrics[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels,
            fill="toself",
            name=row["Model"],
            line=dict(color=MODEL_COLORS[i % len(MODEL_COLORS)], width=2),
            fillcolor=FILL_COLORS[i % len(FILL_COLORS)],
            opacity=0.85,
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=t["radar_title"],
        height=520,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 1],
                gridcolor=C["grid"], linecolor=C["grid"],
                tickfont=dict(color=C["text"], size=9),
            ),
            angularaxis=dict(
                gridcolor=C["grid"], linecolor=C["grid"],
                tickfont=dict(color=C["text_sub"], size=11,
                              family="Syne, sans-serif"),
            ),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Per-model metric breakdown
    st.markdown(f"### {'Per-Model Breakdown' if LANG=='en' else 'تفاصيل كل موديل'}")
    model_cols = st.columns(len(df_models))
    for i, (_, row) in enumerate(df_models.iterrows()):
        color = MODEL_COLORS[i % len(MODEL_COLORS)]
        metrics_html = "".join([f"""
        <div style="display:flex;justify-content:space-between;
                    padding:5px 0;border-bottom:1px solid {C['grid']}">
          <span style="color:{C['text']};font-size:0.78rem">{m}</span>
          <span style="color:{C['text_h']};font-weight:700;font-size:0.78rem">
            {row[m]:.4f}
          </span>
        </div>""" for m in radar_metrics])

        model_cols[i].markdown(f"""
        <div style="background:{C['bg']};border:1px solid {C['border']};
                    border-top:3px solid {color};border-radius:14px;padding:18px">
          <div style="font-family:Syne,sans-serif;font-weight:800;
                      font-size:0.95rem;color:{color};margin-bottom:12px">
            {row['Model']}
          </div>
          {metrics_html}
        </div>
        """, unsafe_allow_html=True)
