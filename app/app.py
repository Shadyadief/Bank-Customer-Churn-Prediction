import streamlit as st
import os

st.set_page_config(
    page_title="Bank Churn Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

from spider import spider
spider()

def load_css():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

THEME = st.session_state.get("theme", "dark")
LANG  = st.session_state.get("lang",  "en")

# ── Palette ────────────────────────────────────────────────────────────────────
if THEME == "dark":
    CARD_BG  = "#111827"
    BG2      = "#0f172a"
    BORDER   = "rgba(0,212,255,0.15)"
    TEXT     = "#94a3b8"
    TEXT_H   = "#f1f5f9"
    TEXT_SUB = "#cbd5e1"
    DIVIDER  = "rgba(0,212,255,0.10)"
    TAG_C    = "#00d4ff"
else:
    CARD_BG  = "#ffffff"
    BG2      = "#e8f0fe"
    BORDER   = "rgba(3,105,161,0.20)"
    TEXT     = "#475569"
    TEXT_H   = "#0f172a"
    TEXT_SUB = "#334155"
    DIVIDER  = "rgba(3,105,161,0.12)"
    TAG_C    = "#0369a1"

# ── Translations ───────────────────────────────────────────────────────────────
T = {
    "en": {
        "title":    "Bank Customer\nChurn Prediction",
        "subtitle": "End-to-end Machine Learning project — powered by XGBoost, Random Forest & Logistic Regression",
        "customers":"Customers","accuracy":"Best Accuracy","roc":"ROC-AUC",
        "models":"ML Models","features":"Features","churn_rate":"Churn Rate",
        "explore": "Explore the Project",
        "go_btn":  "Open page →",
        "wf_title":"⚙️ Project Workflow",
        "st_title":"🛠️ Tech Stack",
        "nav": [
            ("📊","EDA Dashboard","#00d4ff",
             "Explore data and understand churn patterns through interactive visualizations",
             ["Customer distribution analysis","Churn by Geography & Age","Correlation Heatmap"],
             "pages/01_📊_eda_dashboard.py"),
            ("🔮","Churn Predictor","#f43f5e",
             "Enter customer data and get an instant prediction with personalized retention offers",
             ["Real-time ML prediction","Churn probability gauge","Custom retention offers"],
             "pages/02_🔮_predictor.py"),
            ("📈","Model Insights","#10b981",
             "Compare model performance and understand the key factors driving churn",
             ["Model accuracy comparison","Feature importance ranking","Radar performance chart"],
             "pages/03_📈_insights.py"),
        ],
        "workflow": [
            ("01","Data Ingestion","🗂️","Load & validate raw CSV from 10K customers"),
            ("02","Preprocessing","🔧","Clean, encode, scale & apply SMOTE"),
            ("03","EDA","🔍","Explore distributions & churn patterns"),
            ("04","Model Training","🤖","Train XGBoost, Random Forest & LR"),
            ("05","Evaluation","📊","Compare Accuracy, ROC-AUC, F1 & more"),
            ("06","Deployment","🚀","Streamlit app with real-time prediction"),
        ],
    },
    "ar": {
        "title":    "التنبؤ بمغادرة\nعملاء البنك",
        "subtitle": "مشروع تعلم آلة متكامل — مدعوم بـ XGBoost وRandom Forest وLogistic Regression",
        "customers":"عميل","accuracy":"أفضل دقة","roc":"ROC-AUC",
        "models":"موديلات","features":"ميزة","churn_rate":"معدل المغادرة",
        "explore": "استكشف المشروع",
        "go_btn":  "افتح الصفحة →",
        "wf_title":"⚙️ مسار المشروع",
        "st_title":"🛠️ التقنيات المستخدمة",
        "nav": [
            ("📊","لوحة EDA","#00d4ff",
             "استكشف البيانات وافهم أنماط المغادرة عبر رسوم بيانية تفاعلية",
             ["تحليل توزيع العملاء","المغادرة حسب الجغرافيا والعمر","خريطة الارتباط"],
             "pages/01_📊_eda_dashboard.py"),
            ("🔮","توقع المغادرة","#f43f5e",
             "أدخل بيانات العميل واحصل على توقع فوري مع عروض احتفاظ مخصصة",
             ["توقع فوري بالـ ML","مقياس احتمالية المغادرة","عروض احتفاظ مخصصة"],
             "pages/02_🔮_predictor.py"),
            ("📈","رؤى الموديل","#10b981",
             "قارن أداء الموديلات وافهم العوامل الرئيسية المؤثرة على المغادرة",
             ["مقارنة دقة الموديلات","ترتيب أهمية الميزات","رسم رادار الأداء"],
             "pages/03_📈_insights.py"),
        ],
        "workflow": [
            ("01","استيعاب البيانات","🗂️","تحميل والتحقق من بيانات CSV لـ 10K عميل"),
            ("02","المعالجة المسبقة","🔧","تنظيف وترميز وتطبيع ومعالجة الاختلال"),
            ("03","التحليل الاستكشافي","🔍","استكشاف التوزيعات وأنماط المغادرة"),
            ("04","تدريب الموديلات","🤖","تدريب XGBoost وRandom Forest وLR"),
            ("05","التقييم","📊","المقارنة بـ Accuracy وROC-AUC وF1"),
            ("06","النشر","🚀","تطبيق Streamlit بتوقع فوري ورؤى تفاعلية"),
        ],
    },
}
t = T[LANG]

# ── Component CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* equal-height columns */
[data-testid="stHorizontalBlock"] {{ align-items: stretch !important; }}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
    display: flex !important; flex-direction: column !important;
}}

/* ── KPI card ── */
.kpi-card {{
    background: {CARD_BG};
    border-radius: 16px;
    padding: 20px 12px;
    text-align: center;
    height: 100%;
    transition: transform .22s ease, box-shadow .22s ease;
}}
.kpi-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 14px 36px rgba(0,0,0,.28);
}}

/* ── Nav card ── */
.nav-card {{
    background: {CARD_BG};
    border-radius: 20px;
    padding: 26px 22px 20px;
    height: 100%;
    min-height: 265px;
    display: flex;
    flex-direction: column;
    transition: transform .25s cubic-bezier(.22,1,.36,1), box-shadow .25s ease;
    position: relative;
    overflow: hidden;
}}
.nav-card:hover {{
    transform: translateY(-7px);
    box-shadow: 0 22px 50px rgba(0,0,0,.32);
}}
.nav-card .icon  {{ font-size:2rem; margin-bottom:12px; display:inline-block;
                    transition: transform .25s ease; }}
.nav-card:hover .icon {{ transform: scale(1.18) rotate(-4deg); }}
.nav-card .ntitle {{
    font-family: Syne,sans-serif; font-weight:800; font-size:1.1rem;
    color:{TEXT_H}; margin-bottom:9px;
}}
.nav-card .ndesc {{
    font-size:.83rem; color:{TEXT}; line-height:1.65; flex:1; margin-bottom:14px;
}}
.nav-card ul {{
    list-style:none; padding:0; margin:0 0 4px;
}}
.nav-card ul li {{
    font-size:.79rem; color:{TEXT_SUB};
    padding:4px 0; display:flex; align-items:center; gap:7px;
}}
.nav-card ul li::before {{ content:'▸'; font-size:.65rem; opacity:.55; }}

/* ── Step card ── */
.step-card {{
    background: {BG2};
    border-radius: 14px;
    padding: 18px 12px;
    text-align: center;
    height: 100%;
    min-height: 168px;
    display: flex; flex-direction: column; align-items: center;
    transition: transform .22s ease, box-shadow .22s ease;
}}
.step-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,.22);
}}

/* ── Tech card ── */
.tech-card {{
    background: {CARD_BG};
    border-radius: 12px;
    padding: 12px 6px;
    text-align: center;
    height: 100%;
    transition: transform .22s ease, box-shadow .22s ease;
}}
.tech-card:hover {{
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 10px 24px rgba(0,0,0,.2);
}}

/* ── Light mode text clarity ── */
{"" if THEME=="dark" else f"""
.nav-card .ntitle, .nav-card .ndesc, .nav-card ul li,
.step-card, .kpi-card, .tech-card {{
    color: {TEXT_H} !important;
}}
"""}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
lines = t["title"].split("\n")
st.markdown(f"""
<div style="text-align:center;padding:3rem 1rem 2rem">
  <div style="display:inline-flex;align-items:center;justify-content:center;
              width:76px;height:76px;border-radius:20px;
              background:linear-gradient(135deg,#0f4c81,#00d4ff);
              font-size:38px;margin-bottom:1.3rem;
              box-shadow:0 0 40px rgba(0,212,255,.35)">🏦</div>
  <h1 style="font-family:Syne,sans-serif;font-weight:800;
             font-size:clamp(2rem,4vw,3.2rem);
             background:linear-gradient(135deg,#00d4ff 0%,#7c3aed 50%,#10b981 100%);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             line-height:1.15;margin-bottom:1rem">
    {lines[0]}<br>{lines[1]}
  </h1>
  <p style="color:{TEXT};font-size:clamp(.85rem,1.4vw,1rem);
            max-width:680px;margin:0 auto;line-height:1.75">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI
# ══════════════════════════════════════════════════════════════════════════════
STATS = [
    ("10,000",t["customers"], "#00d4ff","rgba(0,212,255,.10)","rgba(0,212,255,.25)"),
    ("87%",   t["accuracy"],  "#10b981","rgba(16,185,129,.10)","rgba(16,185,129,.25)"),
    ("0.88",  t["roc"],       "#7c3aed","rgba(124,58,237,.10)","rgba(124,58,237,.25)"),
    ("3",     t["models"],    "#f59e0b","rgba(245,158,11,.10)","rgba(245,158,11,.25)"),
    ("11",    t["features"],  "#f43f5e","rgba(244,63,94,.10)", "rgba(244,63,94,.25)"),
    ("20.4%", t["churn_rate"],"#00d4ff","rgba(0,212,255,.10)","rgba(0,212,255,.25)"),
]
cols = st.columns(6)
for col, (val, label, color, bg, bdr) in zip(cols, STATS):
    col.markdown(f"""
    <div class="kpi-card"
         style="background:linear-gradient(135deg,{bg},{bg.replace('.10','.03')});
                border:1px solid {bdr};border-top:3px solid {color}">
      <div style="font-family:Syne,sans-serif;font-weight:800;
                  font-size:1.9rem;color:{color};line-height:1">{val}</div>
      <div style="font-size:.68rem;font-weight:700;letter-spacing:.12em;
                  text-transform:uppercase;color:{TEXT};margin-top:7px">{label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2.5rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NAV CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<h2 style="font-family:Syne,sans-serif;font-weight:700;
color:{TEXT_H};margin-bottom:1.4rem">{t["explore"]}</h2>""", unsafe_allow_html=True)

nav_cols = st.columns(3)
for col, (icon, title, color, desc, items, path) in zip(nav_cols, t["nav"]):
    items_html = "".join(f"<li>{i}</li>" for i in items)
    col.markdown(f"""
    <div class="nav-card" style="border:1px solid {BORDER};border-top:4px solid {color}">
      <div class="icon">{icon}</div>
      <div class="ntitle">{title}</div>
      <div class="ndesc">{desc}</div>
      <ul>{items_html}</ul>
    </div>
    """, unsafe_allow_html=True)
    st.page_link(path, label=t["go_btn"])

st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<h2 style="font-family:Syne,sans-serif;font-weight:700;
color:{TEXT_H};margin-bottom:1.4rem">{t["wf_title"]}</h2>""", unsafe_allow_html=True)

STEP_C = ["#00d4ff","#7c3aed","#10b981","#f59e0b","#f43f5e","#3b82f6"]
wf_cols = st.columns(6)
for col, (num, title, icon, desc), color in zip(wf_cols, t["workflow"], STEP_C):
    col.markdown(f"""
    <div class="step-card" style="border:1px solid {color}22;border-top:3px solid {color}">
      <div style="font-size:1.9rem;margin-bottom:8px">{icon}</div>
      <div style="font-family:Syne,sans-serif;font-size:.61rem;font-weight:700;
                  letter-spacing:.18em;text-transform:uppercase;
                  color:{color};margin-bottom:5px">STEP {num}</div>
      <div style="font-family:Syne,sans-serif;font-weight:700;font-size:.84rem;
                  color:{TEXT_H};margin-bottom:7px">{title}</div>
      <div style="font-size:.73rem;color:{TEXT};line-height:1.55">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TECH STACK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""<h2 style="font-family:Syne,sans-serif;font-weight:700;
color:{TEXT_H};margin-bottom:1.4rem">{t["st_title"]}</h2>""", unsafe_allow_html=True)

TECHS = [
    ("Python","#3b82f6","🐍"),("XGBoost","#f59e0b","⚡"),
    ("Scikit-learn","#f43f5e","🔬"),("SMOTE","#10b981","⚖️"),
    ("Streamlit","#ff4b4b","🎈"),("Pandas","#00d4ff","🐼"),
    ("Plotly","#7c3aed","📊"),("Seaborn","#06b6d4","🎨"),
    ("Joblib","#94a3b8","💾"),
]
tech_cols = st.columns(9)
for col, (name, color, icon) in zip(tech_cols, TECHS):
    col.markdown(f"""
    <div class="tech-card" style="border:1px solid {color}35">
      <div style="font-size:1.4rem;margin-bottom:5px">{icon}</div>
      <div style="font-size:.69rem;font-weight:700;color:{color};
                  font-family:Syne,sans-serif;letter-spacing:.03em">{name}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='margin-top:3rem'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid {DIVIDER};padding:24px 0;text-align:center">
  <div style="font-size:.82rem;color:{TEXT}">
    Built with ❤️ by
    <a href="https://www.linkedin.com/in/shadya-dief-ml/" target="_blank"
       style="color:{TAG_C};font-weight:700;text-decoration:none">Eng. Shadya Dief</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
       target="_blank" style="color:{TEXT};text-decoration:none">GitHub ↗</a>
  </div>
</div>
""", unsafe_allow_html=True)
