import streamlit as st
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Spider + CSS ──────────────────────────────────────────────────────────────
from spider import spider
spider()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
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
        "bg":          "#111827",
        "bg2":         "#0f172a",
        "bg3":         "#0d1117",
        "border":      "rgba(0,212,255,0.15)",
        "border2":     "rgba(0,212,255,0.08)",
        "text":        "#94a3b8",
        "text_h":      "#f1f5f9",
        "text_sub":    "#cbd5e1",
        "tag_bg":      "rgba(0,212,255,0.08)",
        "tag_border":  "rgba(0,212,255,0.25)",
        "tag_color":   "#00d4ff",
        "divider":     "rgba(0,212,255,0.10)",
    },
    "light": {
        "bg":          "#ffffff",
        "bg2":         "#f0f6ff",
        "bg3":         "#e8f0fe",
        "border":      "rgba(3,105,161,0.18)",
        "border2":     "rgba(3,105,161,0.08)",
        "text":        "#475569",
        "text_h":      "#0f172a",
        "text_sub":    "#334155",
        "tag_bg":      "rgba(3,105,161,0.07)",
        "tag_border":  "rgba(3,105,161,0.25)",
        "tag_color":   "#0369a1",
        "divider":     "rgba(3,105,161,0.10)",
    },
}[THEME]

# ─── Translations ──────────────────────────────────────────────────────────────
T = {
    "en": {
        "title":       "Bank Customer\nChurn Prediction",
        "subtitle":    "End-to-end Machine Learning project to predict which customers are likely to leave the bank — powered by XGBoost, Random Forest & Logistic Regression",
        "customers":   "Customers",
        "accuracy":    "Best Accuracy",
        "roc":         "ROC-AUC",
        "models":      "ML Models",
        "features":    "Features",
        "churn_rate":  "Churn Rate",
        "explore":     "Explore the Project",
        "eda_title":   "📊 EDA Dashboard",
        "eda_desc":    "Explore the data and understand churn patterns through interactive visualizations",
        "eda_items":   ["Customer distribution analysis", "Churn by Geography & Age", "Correlation Heatmap & insights"],
        "pred_title":  "🔮 Churn Predictor",
        "pred_desc":   "Enter customer data and get an instant churn prediction with personalized retention offers",
        "pred_items":  ["Real-time ML prediction", "Churn probability gauge", "Custom retention offers"],
        "ins_title":   "📈 Model Insights",
        "ins_desc":    "Compare model performance and understand the key factors driving churn",
        "ins_items":   ["Model accuracy comparison", "Feature importance ranking", "Radar performance chart"],
        "go_btn":      "Go to page →",
        "stack_title": "🛠️ Tech Stack",
        "workflow_title": "⚙️ Project Workflow",
        "workflow": [
            ("01", "Data Ingestion",    "🗂️", "Load & validate raw CSV data from 10K bank customers"),
            ("02", "Preprocessing",     "🔧", "Clean, encode, scale & handle class imbalance with SMOTE"),
            ("03", "EDA",               "🔍", "Explore distributions, correlations and churn patterns"),
            ("04", "Model Training",    "🤖", "Train XGBoost, Random Forest & Logistic Regression"),
            ("05", "Evaluation",        "📊", "Compare with Accuracy, ROC-AUC, F1, Precision & Recall"),
            ("06", "Deployment",        "🚀", "Streamlit app with real-time prediction & insights"),
        ],
        "dataset_title": "📂 Dataset",
        "dataset_info":  "Churn Modelling Dataset — 10,000 customers · 14 features",
    },
    "ar": {
        "title":       "التنبؤ بمغادرة\nعملاء البنك",
        "subtitle":    "مشروع تعلم آلة متكامل للتنبؤ بالعملاء المحتمل مغادرتهم للبنك — مدعوم بـ XGBoost وRandom Forest وLogistic Regression",
        "customers":   "عميل",
        "accuracy":    "أفضل دقة",
        "roc":         "ROC-AUC",
        "models":      "موديلات ML",
        "features":    "ميزة",
        "churn_rate":  "معدل المغادرة",
        "explore":     "استكشف المشروع",
        "eda_title":   "📊 لوحة EDA",
        "eda_desc":    "استكشف البيانات وافهم أنماط المغادرة عبر رسوم بيانية تفاعلية",
        "eda_items":   ["تحليل توزيع العملاء", "المغادرة حسب الجغرافيا والعمر", "خريطة الارتباط والرؤى"],
        "pred_title":  "🔮 توقع المغادرة",
        "pred_desc":   "أدخل بيانات العميل واحصل على توقع فوري مع عروض احتفاظ مخصصة",
        "pred_items":  ["توقع فوري بالـ ML", "مقياس احتمالية المغادرة", "عروض احتفاظ مخصصة"],
        "ins_title":   "📈 رؤى الموديل",
        "ins_desc":    "قارن أداء الموديلات وافهم العوامل الرئيسية المؤثرة على المغادرة",
        "ins_items":   ["مقارنة دقة الموديلات", "ترتيب أهمية الميزات", "رسم رادار الأداء"],
        "go_btn":      "انتقل للصفحة →",
        "stack_title": "🛠️ التقنيات المستخدمة",
        "workflow_title": "⚙️ مسار المشروع",
        "workflow": [
            ("01", "استيعاب البيانات", "🗂️", "تحميل والتحقق من بيانات CSV لـ 10K عميل"),
            ("02", "المعالجة المسبقة", "🔧", "تنظيف وترميز وتطبيع البيانات ومعالجة الاختلال"),
            ("03", "التحليل الاستكشافي", "🔍", "استكشاف التوزيعات والارتباطات وأنماط المغادرة"),
            ("04", "تدريب الموديلات",  "🤖", "تدريب XGBoost وRandom Forest وLogistic Regression"),
            ("05", "التقييم",           "📊", "المقارنة بـ Accuracy وROC-AUC وF1 وPrecision وRecall"),
            ("06", "النشر",             "🚀", "تطبيق Streamlit بتوقع فوري ورؤى تفاعلية"),
        ],
        "dataset_title": "📂 مجموعة البيانات",
        "dataset_info":  "Churn Modelling Dataset — 10,000 عميل · 14 ميزة",
    },
}
t = T[LANG]

# ══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════════════════════
title_lines = t["title"].split("\n")
st.markdown(f"""
<div style="text-align:center;padding:3rem 1rem 2rem">
  <div style="display:inline-flex;align-items:center;justify-content:center;
              width:72px;height:72px;border-radius:18px;
              background:linear-gradient(135deg,#0f4c81,#00d4ff);
              font-size:36px;margin-bottom:1.2rem;
              box-shadow:0 0 32px rgba(0,212,255,0.3)">🏦</div>
  <h1 style="font-family:Syne,sans-serif;font-weight:800;font-size:clamp(2rem,4vw,3.2rem);
             background:linear-gradient(135deg,#00d4ff 0%,#7c3aed 50%,#10b981 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             line-height:1.15;margin-bottom:1rem">
    {title_lines[0]}<br>{title_lines[1]}
  </h1>
  <p style="color:{C['text']};font-size:clamp(0.85rem,1.4vw,1rem);
            max-width:680px;margin:0 auto;line-height:1.7">
    {t["subtitle"]}
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI STATS
# ══════════════════════════════════════════════════════════════════════════════
STATS = [
    ("10,000",  t["customers"],  "#00d4ff", "linear-gradient(135deg,rgba(0,212,255,0.12),rgba(0,212,255,0.04))"),
    ("87%",     t["accuracy"],   "#10b981", "linear-gradient(135deg,rgba(16,185,129,0.12),rgba(16,185,129,0.04))"),
    ("0.88",    t["roc"],        "#7c3aed", "linear-gradient(135deg,rgba(124,58,237,0.12),rgba(124,58,237,0.04))"),
    ("3",       t["models"],     "#f59e0b", "linear-gradient(135deg,rgba(245,158,11,0.12),rgba(245,158,11,0.04))"),
    ("11",      t["features"],   "#f43f5e", "linear-gradient(135deg,rgba(244,63,94,0.12),rgba(244,63,94,0.04))"),
    ("20.4%",   t["churn_rate"], "#00d4ff", "linear-gradient(135deg,rgba(0,212,255,0.12),rgba(0,212,255,0.04))"),
]

cols = st.columns(len(STATS))
for col, (val, label, color, grad) in zip(cols, STATS):
    col.markdown(f"""
    <div style="background:{grad};border:1px solid {color}22;
                border-top:3px solid {color};border-radius:16px;
                padding:20px 14px;text-align:center">
      <div style="font-family:Syne,sans-serif;font-weight:800;
                  font-size:1.8rem;color:{color};line-height:1">{val}</div>
      <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.10em;
                  text-transform:uppercase;color:{C['text']};margin-top:6px">
        {label}
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NAV CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h2 style="font-family:Syne,sans-serif;font-weight:700;color:{C['text_h']};
           margin-bottom:1.2rem">{t["explore"]}</h2>
""", unsafe_allow_html=True)

NAV_PAGES = [
    (t["eda_title"],  t["eda_desc"],  t["eda_items"],  "#00d4ff",
     "pages/01_📊_eda_dashboard.py"),
    (t["pred_title"], t["pred_desc"], t["pred_items"], "#f43f5e",
     "pages/02_🔮_predictor.py"),
    (t["ins_title"],  t["ins_desc"],  t["ins_items"],  "#10b981",
     "pages/03_📈_insights.py"),
]

nav_cols = st.columns(3)
for col, (title, desc, items, color, path) in zip(nav_cols, NAV_PAGES):
    items_html = "".join([
        f'<li style="margin-bottom:5px;color:{C["text_sub"]}">{item}</li>'
        for item in items
    ])
    col.markdown(f"""
    <div style="background:{C['bg']};border:1px solid {C['border']};
                border-top:4px solid {color};border-radius:18px;
                padding:26px 22px;height:100%;
                transition:all 0.25s;cursor:default">
      <div style="font-family:Syne,sans-serif;font-weight:800;font-size:1.1rem;
                  color:{C['text_h']};margin-bottom:10px">{title}</div>
      <div style="font-size:0.83rem;color:{C['text']};line-height:1.6;
                  margin-bottom:14px">{desc}</div>
      <ul style="padding-left:16px;font-size:0.82rem;margin:0 0 18px">
        {items_html}
      </ul>
    </div>
    """, unsafe_allow_html=True)
    st.page_link(path, label=t["go_btn"])
    st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW TIMELINE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h2 style="font-family:Syne,sans-serif;font-weight:700;color:{C['text_h']};
           margin-bottom:1.2rem">{t["workflow_title"]}</h2>
""", unsafe_allow_html=True)

wf_cols = st.columns(len(t["workflow"]))
STEP_COLORS = ["#00d4ff","#7c3aed","#10b981","#f59e0b","#f43f5e","#3b82f6"]

for col, (num, title, icon, desc), color in zip(wf_cols, t["workflow"], STEP_COLORS):
    col.markdown(f"""
    <div style="background:{C['bg2']};border:1px solid {color}22;
                border-radius:14px;padding:18px 14px;text-align:center;
                position:relative">
      <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
      <div style="font-family:Syne,sans-serif;font-size:0.65rem;font-weight:700;
                  letter-spacing:0.15em;text-transform:uppercase;
                  color:{color};margin-bottom:6px">STEP {num}</div>
      <div style="font-family:Syne,sans-serif;font-weight:700;font-size:0.88rem;
                  color:{C['text_h']};margin-bottom:8px">{title}</div>
      <div style="font-size:0.75rem;color:{C['text']};line-height:1.55">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TECH STACK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h2 style="font-family:Syne,sans-serif;font-weight:700;color:{C['text_h']};
           margin-bottom:1.2rem">{t["stack_title"]}</h2>
""", unsafe_allow_html=True)

TECHS = [
    ("Python",       "#3b82f6", "🐍"),
    ("XGBoost",      "#f59e0b", "⚡"),
    ("Scikit-learn", "#f43f5e", "🔬"),
    ("SMOTE",        "#10b981", "⚖️"),
    ("Streamlit",    "#ff4b4b", "🎈"),
    ("Pandas",       "#00d4ff", "🐼"),
    ("Plotly",       "#7c3aed", "📊"),
    ("Seaborn",      "#06b6d4", "🎨"),
    ("Joblib",       "#94a3b8", "💾"),
]

tech_cols = st.columns(len(TECHS))
for col, (name, color, icon) in zip(tech_cols, TECHS):
    col.markdown(f"""
    <div style="background:{C['bg']};border:1px solid {color}33;
                border-radius:10px;padding:10px 6px;text-align:center">
      <div style="font-size:1.3rem;margin-bottom:4px">{icon}</div>
      <div style="font-size:0.72rem;font-weight:700;color:{color};
                  font-family:Syne,sans-serif;letter-spacing:0.02em">{name}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid {C['divider']};padding:24px 0;text-align:center">
  <div style="font-size:0.8rem;color:{C['text']}">
    Built with ❤️ by
    <a href="https://www.linkedin.com/in/shadya-dief-ml/"
       target="_blank"
       style="color:{C['tag_color']};font-weight:700;text-decoration:none">
      Eng. Shadya Dief
    </a>
    &nbsp;·&nbsp;
    <a href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
       target="_blank"
       style="color:{C['text']};text-decoration:none">
      GitHub ↗
    </a>
  </div>
</div>
""", unsafe_allow_html=True)
