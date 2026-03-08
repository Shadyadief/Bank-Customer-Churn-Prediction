import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
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
    "dark":  {
        "bg":        "#111827",
        "bg2":       "#0f172a",
        "border":    "rgba(0,212,255,0.15)",
        "text":      "#94a3b8",
        "text_h":    "#f1f5f9",
        "text_sub":  "#cbd5e1",
        "card_risk_high":   "rgba(244,63,94,0.10)",
        "card_risk_med":    "rgba(245,158,11,0.10)",
        "card_risk_low":    "rgba(16,185,129,0.10)",
        "border_risk_high": "#f43f5e",
        "border_risk_med":  "#f59e0b",
        "border_risk_low":  "#10b981",
        "offer_bg":         "#1a2235",
        "offer_text":       "#cbd5e1",
        "gauge_bg":         "rgba(0,0,0,0)",
    },
    "light": {
        "bg":        "#ffffff",
        "bg2":       "#f0f6ff",
        "border":    "rgba(3,105,161,0.18)",
        "text":      "#475569",
        "text_h":    "#0f172a",
        "text_sub":  "#334155",
        "card_risk_high":   "rgba(244,63,94,0.07)",
        "card_risk_med":    "rgba(245,158,11,0.07)",
        "card_risk_low":    "rgba(16,185,129,0.07)",
        "border_risk_high": "#e11d48",
        "border_risk_med":  "#d97706",
        "border_risk_low":  "#059669",
        "offer_bg":         "#f8fafc",
        "offer_text":       "#334155",
        "gauge_bg":         "rgba(0,0,0,0)",
    },
}[THEME]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color=C["text"], size=12),
    margin=dict(t=40, b=10, l=10, r=10),
)

# ─── Translations ──────────────────────────────────────────────────────────────
T = {
    "en": {
        "title":          "🔮 Churn Predictor",
        "subtitle":       "Enter customer data and predict whether they will churn",
        "model_warn":     "⚠️ Model not found! Run training first.",
        "form_title":     "📝 Customer Information",
        "credit":         "💳 Credit Score",
        "age":            "🎂 Age",
        "tenure":         "📅 Tenure (years)",
        "balance":        "💰 Balance ($)",
        "products":       "📦 Number of Products",
        "has_card":       "💳 Has Credit Card?",
        "is_active":      "✅ Is Active Member?",
        "salary":         "💵 Estimated Salary ($)",
        "geography":      "🌍 Geography",
        "gender":         "👤 Gender",
        "yes":            "Yes",
        "no":             "No",
        "predict_btn":    "🔮 Predict Churn",
        "result_title":   "📊 Prediction Result",
        "will_churn":     "🔴 Will Churn",
        "no_churn":       "🟢 Will Stay",
        "churn_prob":     "Churn Probability",
        "risk_high":      "🚨 HIGH RISK — Immediate action required",
        "risk_med":       "⚠️ MEDIUM RISK — Monitor closely",
        "risk_low":       "✅ LOW RISK — Customer is stable",
        "offers_title":   "💡 Personalized Retention Offers",
        "offers_sub":     "offers suggested based on customer profile",
        "stable_title":   "💡 Recommendations",
        "stable_body":    "Customer is stable — Focus on Engagement",
        "stable_tips":    ["🌟 Offer a loyalty points program",
                           "📈 Suggest additional suitable products",
                           "📬 Send periodic offers to keep them active"],
        "input_summary":  "📋 Input Summary",
        "feature":        "Feature",
        "value":          "Value",
        "male":           "Male",
        "female":         "Female",
    },
    "ar": {
        "title":          "🔮 توقع المغادرة",
        "subtitle":       "أدخل بيانات العميل لمعرفة احتمالية مغادرته",
        "model_warn":     "⚠️ الموديل غير موجود! قم بتشغيل التدريب أولاً.",
        "form_title":     "📝 بيانات العميل",
        "credit":         "💳 درجة الائتمان",
        "age":            "🎂 العمر",
        "tenure":         "📅 سنوات العضوية",
        "balance":        "💰 الرصيد ($)",
        "products":       "📦 عدد المنتجات",
        "has_card":       "💳 يملك بطاقة ائتمان؟",
        "is_active":      "✅ عضو نشط؟",
        "salary":         "💵 الراتب المتوقع ($)",
        "geography":      "🌍 الدولة",
        "gender":         "👤 الجنس",
        "yes":            "نعم",
        "no":             "لا",
        "predict_btn":    "🔮 توقع المغادرة",
        "result_title":   "📊 نتيجة التوقع",
        "will_churn":     "🔴 سيغادر البنك",
        "no_churn":       "🟢 سيبقى مع البنك",
        "churn_prob":     "احتمالية المغادرة",
        "risk_high":      "🚨 خطر عالي — يحتاج تدخل فوري",
        "risk_med":       "⚠️ خطر متوسط — راقبه عن كثب",
        "risk_low":       "✅ خطر منخفض — العميل مستقر",
        "offers_title":   "💡 عروض مخصصة للاحتفاظ بالعميل",
        "offers_sub":     "عرض مقترح بناءً على ملف العميل",
        "stable_title":   "💡 التوصيات",
        "stable_body":    "العميل مستقر — ركّز على التفاعل معه",
        "stable_tips":    ["🌟 قدّم له برنامج نقاط الولاء",
                           "📈 اقترح منتجات إضافية مناسبة",
                           "📬 راسله بعروض دورية عشان يفضل نشط"],
        "input_summary":  "📋 ملخص البيانات المدخلة",
        "feature":        "الميزة",
        "value":          "القيمة",
        "male":           "ذكر",
        "female":         "أنثى",
    },
}
t = T[LANG]

# ─── Load Model & Scaler ───────────────────────────────────────────────────────
@st.cache_resource
def load_model_and_scaler():
    base   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model  = joblib.load(os.path.join(base, "models", "xgboost_model.pkl"))
    scaler = joblib.load(os.path.join(base, "models", "scaler.pkl"))
    return model, scaler

try:
    model, scaler = load_model_and_scaler()
    model_loaded  = True
except Exception:
    model_loaded  = False

# ─── Recommendation Engine ─────────────────────────────────────────────────────
def get_recommendations(customer: dict, prediction: int, lang: str) -> list:
    if prediction == 0:
        return []

    offers_en = {
        "cashback": {
            "icon": "🎁", "title": "CashBack Activation Offer",
            "desc": "Get 5% cashback for 3 months upon account activation",
            "tag": "Engagement",
        },
        "credit_card": {
            "icon": "💳", "title": "Premium Credit Card — Free First Year",
            "desc": "Free premium credit card for the first year with exclusive benefits",
            "tag": "Product",
        },
        "high_yield": {
            "icon": "📈", "title": "High-Yield Savings Account",
            "desc": "8% annual interest on balances above $100,000",
            "tag": "Financial",
        },
        "savings": {
            "icon": "💰", "title": "Savings Boost Plan",
            "desc": "5% interest on your current balance for 6 months",
            "tag": "Financial",
        },
        "retirement": {
            "icon": "🏦", "title": "Retirement Investment Plan",
            "desc": "Guaranteed-return retirement savings plan",
            "tag": "Investment",
        },
        "first_card": {
            "icon": "💳", "title": "First Credit Card — Zero Fees",
            "desc": "Credit card with no annual fees for the first year",
            "tag": "Product",
        },
        "germany": {
            "icon": "🇩🇪", "title": "Loyalty Reward — Germany Exclusive",
            "desc": "Double points loyalty program exclusive to Germany customers",
            "tag": "Loyalty",
        },
        "vip": {
            "icon": "⭐", "title": "VIP Loyalty Program",
            "desc": "Join the VIP program and get exclusive benefits",
            "tag": "Loyalty",
        },
    }

    offers_ar = {
        "cashback": {
            "icon": "🎁", "title": "عرض تفعيل كاش باك",
            "desc": "احصل على 5% كاش باك لمدة 3 شهور عند تفعيل حسابك",
            "tag": "تفاعل",
        },
        "credit_card": {
            "icon": "💳", "title": "بطاقة ائتمان بريميوم — مجانية السنة الأولى",
            "desc": "بطاقة ائتمان مجانية السنة الأولى مع مزايا حصرية",
            "tag": "منتج",
        },
        "high_yield": {
            "icon": "📈", "title": "حساب توفير عالي العائد",
            "desc": "فائدة 8% سنوياً على الأرصدة فوق 100,000$",
            "tag": "مالي",
        },
        "savings": {
            "icon": "💰", "title": "خطة تعزيز المدخرات",
            "desc": "فائدة 5% على رصيدك الحالي لمدة 6 شهور",
            "tag": "مالي",
        },
        "retirement": {
            "icon": "🏦", "title": "خطة استثمار التقاعد",
            "desc": "خطة ادخار للتقاعد بعوائد مضمونة",
            "tag": "استثمار",
        },
        "first_card": {
            "icon": "💳", "title": "أول بطاقة ائتمان — بدون رسوم",
            "desc": "بطاقة ائتمان بدون رسوم سنوية للسنة الأولى",
            "tag": "منتج",
        },
        "germany": {
            "icon": "🇩🇪", "title": "مكافأة الولاء — حصري ألمانيا",
            "desc": "برنامج نقاط مضاعفة حصري لعملاء ألمانيا",
            "tag": "ولاء",
        },
        "vip": {
            "icon": "⭐", "title": "برنامج VIP للولاء",
            "desc": "انضم لبرنامج VIP واحصل على مزايا حصرية",
            "tag": "ولاء",
        },
    }

    pool   = offers_ar if lang == "ar" else offers_en
    result = []

    if customer["IsActiveMember"]    == 0: result.append(pool["cashback"])
    if customer["NumOfProducts"]     == 1: result.append(pool["credit_card"])
    if customer["Balance"]      > 100_000: result.append(pool["high_yield"])
    elif customer["Balance"]         >  0: result.append(pool["savings"])
    if customer["Age"]               > 50: result.append(pool["retirement"])
    if customer["HasCrCard"]         == 0: result.append(pool["first_card"])
    if customer["Geography_Germany"] == 1: result.append(pool["germany"])
    if not result:                         result.append(pool["vip"])

    return result


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-bottom:2rem">
  <h1 style="font-family:Syne,sans-serif;font-weight:800;
             background:linear-gradient(135deg,#7c3aed,#00d4ff);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             margin-bottom:6px">{t["title"]}</h1>
  <p style="color:{C['text']};font-size:0.9rem;margin:0">{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.warning(t["model_warn"])
    st.code("python src/models/train_model.py", language="bash")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:{C['bg']};border:1px solid {C['border']};
            border-radius:16px;padding:24px 28px;margin-bottom:1.5rem">
  <h3 style="font-family:Syne,sans-serif;color:{C['text_h']};margin:0 0 20px">
    {t["form_title"]}
  </h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.slider(t["credit"],   300, 850, 650)
    age          = st.slider(t["age"],       18,  92,  35)
    tenure       = st.slider(t["tenure"],     0,  10,   5)
    balance      = st.number_input(t["balance"],   0.0, 250_000.0, 50_000.0, 1_000.0)

with col2:
    num_products = st.selectbox(t["products"], [1, 2, 3, 4])
    has_cr_card  = st.selectbox(t["has_card"], [t["yes"], t["no"]])
    is_active    = st.selectbox(t["is_active"],[t["yes"], t["no"]])
    salary       = st.number_input(t["salary"],0.0, 200_000.0, 75_000.0, 1_000.0)

with col3:
    geography    = st.selectbox(t["geography"], ["France", "Germany", "Spain"])
    gender       = st.selectbox(t["gender"],    [t["male"], t["female"]])
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Mini risk indicator ──
    rough_risk = 0
    if age > 50:          rough_risk += 2
    if num_products >= 3: rough_risk += 3
    if is_active == t["no"]:  rough_risk += 2
    if balance == 0:      rough_risk += 1
    if geography == "Germany": rough_risk += 1

    risk_pct = min(rough_risk / 9 * 100, 100)
    risk_color = "#f43f5e" if risk_pct > 60 else "#f59e0b" if risk_pct > 35 else "#10b981"
    st.markdown(f"""
    <div style="background:{C['bg2']};border:1px solid {C['border']};
                border-radius:12px;padding:14px;text-align:center">
      <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.12em;
                  text-transform:uppercase;color:{C['text']};margin-bottom:8px">
        Quick Risk Estimate
      </div>
      <div style="font-size:1.6rem;font-weight:800;font-family:Syne,sans-serif;
                  color:{risk_color}">{risk_pct:.0f}%</div>
      <div style="background:{C['bg']};border-radius:6px;height:6px;margin-top:8px">
        <div style="background:{risk_color};width:{risk_pct}%;height:6px;
                    border-radius:6px;transition:width 0.3s"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Predict Button ────────────────────────────────────────────────────────────
predict_btn = st.button(t["predict_btn"], type="primary", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PREDICTION RESULT
# ══════════════════════════════════════════════════════════════════════════════
if predict_btn:
    is_yes    = t["yes"]
    is_male   = t["male"]

    input_dict = {
        "CreditScore":       credit_score,
        "Age":               age,
        "Tenure":            tenure,
        "Balance":           balance,
        "NumOfProducts":     num_products,
        "HasCrCard":         1 if has_cr_card == is_yes else 0,
        "IsActiveMember":    1 if is_active   == is_yes else 0,
        "EstimatedSalary":   salary,
        "Gender_Male":       1 if gender      == is_male else 0,
        "Geography_Germany": 1 if geography   == "Germany" else 0,
        "Geography_Spain":   1 if geography   == "Spain"   else 0,
    }

    input_df     = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)
    prediction   = model.predict(input_scaled)[0]
    probability  = model.predict_proba(input_scaled)[0][1]

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Result + Gauge ──────────────────────────────────────────────────────
    res_col, gauge_col = st.columns([1, 1])

    with res_col:
        is_churn    = prediction == 1
        card_bg     = C["card_risk_high"] if is_churn else C["card_risk_low"]
        card_border = C["border_risk_high"] if is_churn else C["border_risk_low"]
        label       = t["will_churn"] if is_churn else t["no_churn"]

        if probability >= 0.7:
            risk_msg   = t["risk_high"]
            risk_color = "#f43f5e"
        elif probability >= 0.5:
            risk_msg   = t["risk_med"]
            risk_color = "#f59e0b"
        else:
            risk_msg   = t["risk_low"]
            risk_color = "#10b981"

        st.markdown(f"""
        <div style="background:{card_bg};border:2px solid {card_border};
                    border-radius:18px;padding:28px;height:100%">
          <div style="font-family:Syne,sans-serif;font-size:1.6rem;
                      font-weight:800;color:{card_border};margin-bottom:12px">
            {label}
          </div>
          <div style="font-size:0.85rem;color:{C['text']};margin-bottom:16px">
            {t["churn_prob"]}
          </div>
          <div style="font-family:Syne,sans-serif;font-size:3rem;
                      font-weight:800;color:{card_border};line-height:1;margin-bottom:16px">
            {probability*100:.1f}%
          </div>
          <div style="background:{card_border};opacity:0.15;height:6px;
                      border-radius:6px;margin-bottom:16px">
          </div>
          <div style="background:rgba(0,0,0,0.1);border-radius:6px;height:6px;margin-bottom:16px">
            <div style="background:{card_border};width:{probability*100:.1f}%;
                        height:6px;border-radius:6px"></div>
          </div>
          <div style="font-size:0.85rem;font-weight:700;color:{risk_color}">
            {risk_msg}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with gauge_col:
        gauge_color = "#f43f5e" if probability > 0.5 else "#10b981"
        fig = go.Figure(go.Indicator(
            mode  = "gauge+number+delta",
            value = probability * 100,
            delta = {"reference": 50, "increasing": {"color": "#f43f5e"},
                                       "decreasing": {"color": "#10b981"}},
            number= {"suffix": "%", "font": {"size": 42, "family": "Syne, sans-serif",
                                             "color": C["text_h"]}},
            title = {"text": t["churn_prob"],
                     "font": {"size": 14, "family": "Syne, sans-serif", "color": C["text"]}},
            gauge = {
                "axis":  {"range": [0, 100], "tickcolor": C["text"],
                          "tickfont": {"color": C["text"], "size": 10}},
                "bar":   {"color": gauge_color, "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "bordercolor": C["border"],
                "steps": [
                    {"range": [0,  40], "color": "rgba(16,185,129,0.12)"},
                    {"range": [40, 65], "color": "rgba(245,158,11,0.12)"},
                    {"range": [65,100], "color": "rgba(244,63,94,0.12)"},
                ],
                "threshold": {
                    "line": {"color": "#ffffff", "width": 3},
                    "thickness": 0.8,
                    "value": 50,
                },
            },
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Input Summary ───────────────────────────────────────────────────────
    with st.expander(t["input_summary"]):
        summary_data = {
            t["feature"]: [
                "Credit Score","Age","Tenure","Balance ($)",
                "Num of Products","Has Credit Card","Is Active",
                "Salary ($)","Geography","Gender"
            ],
            t["value"]: [
                credit_score, age, tenure, f"{balance:,.0f}",
                num_products, has_cr_card, is_active,
                f"{salary:,.0f}", geography, gender
            ],
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    # ── Recommendations / Offers ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    recommendations = get_recommendations(input_dict, prediction, LANG)

    TAG_COLORS = {
        "Engagement": "#00d4ff", "Product": "#7c3aed",
        "Financial": "#10b981",  "Investment": "#f59e0b",
        "Loyalty": "#f43f5e",
        # Arabic
        "تفاعل": "#00d4ff", "منتج": "#7c3aed",
        "مالي": "#10b981",  "استثمار": "#f59e0b",
        "ولاء": "#f43f5e",
    }

    if prediction == 1 and recommendations:
        st.markdown(f"""
        <h3 style="font-family:Syne,sans-serif;color:{C['text_h']};margin-bottom:6px">
          {t["offers_title"]}
        </h3>
        <p style="color:{C['text']};font-size:0.82rem;margin-bottom:20px">
          {len(recommendations)} {t["offers_sub"]}
        </p>
        """, unsafe_allow_html=True)

        cols = st.columns(min(len(recommendations), 3))
        for i, offer in enumerate(recommendations):
            tag_color = TAG_COLORS.get(offer["tag"], "#00d4ff")
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:{C['bg']};border:1px solid {C['border']};
                            border-top:3px solid {tag_color};
                            border-radius:14px;padding:20px;margin-bottom:14px;
                            transition:all 0.2s">
                  <div style="display:flex;justify-content:space-between;
                              align-items:flex-start;margin-bottom:10px">
                    <span style="font-size:1.8rem">{offer['icon']}</span>
                    <span style="background:rgba(0,0,0,0.15);color:{tag_color};
                                 font-size:0.65rem;font-weight:700;
                                 letter-spacing:0.1em;text-transform:uppercase;
                                 padding:3px 8px;border-radius:20px;
                                 border:1px solid {tag_color}">
                      {offer['tag']}
                    </span>
                  </div>
                  <div style="font-family:Syne,sans-serif;font-weight:700;
                              font-size:0.95rem;color:{C['text_h']};margin-bottom:8px">
                    {offer['title']}
                  </div>
                  <div style="font-size:0.82rem;color:{C['text']};line-height:1.55">
                    {offer['desc']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    elif prediction == 0:
        tips_html = "".join([f"<li style='margin-bottom:6px'>{tip}</li>"
                             for tip in t["stable_tips"]])
        st.markdown(f"""
        <div style="background:{C['card_risk_low']};
                    border:1px solid {C['border_risk_low']};
                    border-left:4px solid {C['border_risk_low']};
                    border-radius:14px;padding:24px">
          <div style="font-family:Syne,sans-serif;font-weight:700;
                      font-size:1.05rem;color:{C['border_risk_low']};margin-bottom:12px">
            ✅ {t["stable_body"]}
          </div>
          <ul style="color:{C['text_sub']};font-size:0.88rem;
                     line-height:1.7;margin:0;padding-left:20px">
            {tips_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)
