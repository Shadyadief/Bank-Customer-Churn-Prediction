import streamlit as st
import os

# ═══════════════════════════════════════════════════════════════════
#  spider.py — Shared Sidebar for ALL pages
#  Project : Bank Customer Churn Prediction
#  Author  : Eng. Shadya Dief
# ═══════════════════════════════════════════════════════════════════

# ── Navigation pages ───────────────────────────────────────────────
NAV = [
    ("📊", "EDA Dashboard",   "لوحة التحليل",    "pages/01_📊_eda_dashboard.py"),
    ("🔮", "Predictor",       "توقع المغادرة",   "pages/02_🔮_predictor.py"),
    ("📈", "Model Insights",  "رؤى الموديل",     "pages/03_📈_insights.py"),
]


def spider():
    """
    ضيفي في أول كل صفحة:

        from spider import spider
        spider()

    يرجع: (theme, lang)
        st.session_state.theme  →  'dark' | 'light'
        st.session_state.lang   →  'en'   | 'ar'
    """

    # ── Init session state ─────────────────────────────────────────
    if "theme"        not in st.session_state: st.session_state.theme        = "dark"
    if "lang"         not in st.session_state: st.session_state.lang         = "en"
    if "sidebar_open" not in st.session_state: st.session_state.sidebar_open = True

    THEME = st.session_state.theme
    LANG  = st.session_state.lang

    # ── Color Palette ──────────────────────────────────────────────
    if THEME == "dark":
        NAV_BG   = "#0a0e1a"
        NAV_BG2  = "#0f172a"
        ACCENT   = "#00d4ff"
        ACCENT2  = "#7c3aed"
        WHITE    = "#f1f5f9"
        GREY     = "#64748b"
        BORDER   = "rgba(0,212,255,0.12)"
        BORDER2  = "rgba(0,212,255,0.06)"
        BTN_BG   = "rgba(0,212,255,0.06)"
        BTN_HV   = "rgba(0,212,255,0.15)"
        TGL_BG   = "rgba(255,255,255,0.05)"
        TGL_HV   = "rgba(255,255,255,0.10)"
        ICON_BG  = "rgba(0,212,255,0.10)"
        ICON_HV  = "rgba(0,212,255,0.22)"
    else:
        NAV_BG   = "#f0f6ff"
        NAV_BG2  = "#e8f0fe"
        ACCENT   = "#0369a1"
        ACCENT2  = "#6d28d9"
        WHITE    = "#0f172a"
        GREY     = "#64748b"
        BORDER   = "rgba(3,105,161,0.15)"
        BORDER2  = "rgba(3,105,161,0.07)"
        BTN_BG   = "rgba(3,105,161,0.06)"
        BTN_HV   = "rgba(3,105,161,0.14)"
        TGL_BG   = "rgba(0,0,0,0.05)"
        TGL_HV   = "rgba(0,0,0,0.10)"
        ICON_BG  = "rgba(3,105,161,0.10)"
        ICON_HV  = "rgba(3,105,161,0.22)"

    FF = "Tajawal" if LANG == "ar" else "Syne"

    # ── Global CSS ─────────────────────────────────────────────────
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@400;500&family=Tajawal:wght@400;700;800&display=swap');

    /* ── Sidebar base ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAV_BG} 0%, {NAV_BG2} 100%) !important;
        border-right: 1px solid {BORDER} !important;
        min-width: 230px !important;
    }}
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {{
        color: {WHITE} !important;
        font-family: '{FF}', sans-serif !important;
    }}

    /* ── ALL sidebar buttons base ── */
    [data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: 1px solid transparent !important;
        color: {GREY} !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-size: .83rem !important;
        font-weight: 600 !important;
        padding: 9px 12px !important;
        margin-bottom: 3px !important;
        transition: all .18s ease !important;
        font-family: '{FF}', sans-serif !important;
        text-align: left !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: {BTN_HV} !important;
        color: {ACCENT} !important;
        border-color: {BORDER} !important;
    }}

    /* ── NAV icon buttons ── */
    .nav-icon-btn .stButton > button {{
        background: {ICON_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {WHITE} !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        margin-bottom: 5px !important;
        font-size: .85rem !important;
        font-weight: 700 !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        transition: all .2s ease !important;
    }}
    .nav-icon-btn .stButton > button:hover {{
        background: {ICON_HV} !important;
        border-color: {ACCENT} !important;
        color: {ACCENT} !important;
        transform: translateX(3px) !important;
        box-shadow: 0 0 12px {BORDER} !important;
    }}

    /* ── Toggle buttons ── */
    .tgl-btn .stButton > button {{
        background: {TGL_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {WHITE} !important;
        border-radius: 20px !important;
        padding: 7px 10px !important;
        font-size: .78rem !important;
        font-weight: 700 !important;
        letter-spacing: .03em !important;
    }}
    .tgl-btn .stButton > button:hover {{
        background: {BTN_HV} !important;
        border-color: {ACCENT} !important;
        color: {ACCENT} !important;
    }}

    /* ── Divider ── */
    .sp-divider {{
        height: 1px;
        background: {BORDER};
        margin: 10px 0;
    }}

    /* ── App bg ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {'#07090f' if THEME == 'dark' else '#f0f6ff'} !important;
        color: {WHITE} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:

        # ── 1. Project Logo + Name ─────────────────────────────────
        st.markdown(f"""
        <div style="text-align:center;padding:22px 12px 16px;
                    border-bottom:1px solid {BORDER}">
          <div style="width:60px;height:60px;border-radius:16px;
                      background:linear-gradient(135deg,#0f4c81,#00d4ff);
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 11px;font-size:28px;
                      box-shadow:0 4px 20px rgba(0,212,255,0.22)">🏦</div>
          <div style="font-family:'{FF}',sans-serif;font-weight:800;
                      font-size:13px;color:{WHITE};line-height:1.45;margin-bottom:5px">
            {'التنبؤ بمغادرة العملاء' if LANG == 'ar' else 'Bank Customer<br>Churn Prediction'}
          </div>
          <div style="font-size:10px;color:{ACCENT};letter-spacing:1.3px;
                      text-transform:uppercase;font-weight:600">
            ML · Classification
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. Profile + Social Links ──────────────────────────────
        st.markdown(f"""
        <div style="text-align:center;padding:16px 12px 14px;
                    border-bottom:1px solid {BORDER}">
          <div style="width:52px;height:52px;border-radius:50%;
                      background:linear-gradient(135deg,#00d4ff,#7c3aed);
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 8px;font-size:22px;
                      box-shadow:0 0 14px rgba(0,212,255,0.22)">👩‍💻</div>
          <div style="font-family:'{FF}',sans-serif;font-weight:800;
                      font-size:13.5px;color:{WHITE};margin-bottom:3px">
            Eng. Shadya Dief
          </div>
          <div style="font-size:9.5px;color:{ACCENT};letter-spacing:1.3px;
                      text-transform:uppercase;font-weight:600;margin-bottom:12px">
            {'مهندسة تعلم الآلة' if LANG == 'ar' else 'ML Engineer'}
          </div>
          <div style="display:flex;gap:7px;justify-content:center">
            <a href="https://www.linkedin.com/in/shadya-dief-ml/"
               target="_blank"
               style="display:flex;align-items:center;gap:5px;
                      padding:5px 11px;border-radius:20px;font-size:10.5px;
                      font-weight:700;text-decoration:none;
                      background:rgba(10,102,194,0.15);
                      border:1px solid rgba(10,102,194,0.40);
                      color:#60a5fa;transition:all .2s">
              in LinkedIn
            </a>
            <a href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
               target="_blank"
               style="display:flex;align-items:center;gap:5px;
                      padding:5px 11px;border-radius:20px;font-size:10.5px;
                      font-weight:700;text-decoration:none;
                      background:{TGL_BG};border:1px solid {BORDER};
                      color:{WHITE};transition:all .2s">
              ⌥ GitHub
            </a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3. Theme + Language Toggles ────────────────────────────
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown('<div class="tgl-btn">', unsafe_allow_html=True)
            theme_lbl = ("☀️ Light" if THEME == "dark" else "🌙 Dark")
            if st.button(theme_lbl, key="sp_theme", use_container_width=True):
                st.session_state.theme = "light" if THEME == "dark" else "dark"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with tc2:
            st.markdown('<div class="tgl-btn">', unsafe_allow_html=True)
            lang_lbl = ("🌐 عربي" if LANG == "en" else "🌐 English")
            if st.button(lang_lbl, key="sp_lang", use_container_width=True):
                st.session_state.lang = "ar" if LANG == "en" else "en"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── 4. Navigation ──────────────────────────────────────────
        nav_label = "التنقل" if LANG == "ar" else "NAVIGATION"
        st.markdown(f"""
        <div style="font-size:9px;font-weight:700;letter-spacing:1.8px;
                    text-transform:uppercase;color:{GREY};
                    padding:14px 4px 6px;opacity:0.7">
          📌 {nav_label}
        </div>
        """, unsafe_allow_html=True)

        for icon, en_lbl, ar_lbl, fpath in NAV:
            label = f"{icon}  {ar_lbl}" if LANG == "ar" else f"{icon}  {en_lbl}"
            key   = "sp_nav_" + os.path.basename(fpath).replace(" ", "_")
            st.markdown('<div class="nav-icon-btn">', unsafe_allow_html=True)
            if st.button(label, key=key, use_container_width=True):
                st.switch_page(fpath)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── 5. Footer ──────────────────────────────────────────────
        st.markdown(f"""
        <div style="height:1px;background:{BORDER};margin:14px 0 10px"></div>
        <div style="font-size:.67rem;color:{GREY};padding:0 2px;
                    line-height:1.9;text-align:center">
          Built with ❤️ by
          <a href="https://www.linkedin.com/in/shadya-dief-ml/"
             target="_blank"
             style="color:{ACCENT};text-decoration:none;font-weight:700">
            Eng. Shadya Dief
          </a>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.theme, st.session_state.lang
