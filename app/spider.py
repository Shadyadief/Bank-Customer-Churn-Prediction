import streamlit as st
import os

# ═══════════════════════════════════════════════════════════════════
#  spider.py — Shared Sidebar for ALL pages
#  Project : Bank Customer Churn Prediction
#  Author  : Eng. Shadya Dief
# ═══════════════════════════════════════════════════════════════════

NAV = [
    ("📊", "EDA Dashboard",  "لوحة التحليل",  "pages/01_📊_eda_dashboard.py"),
    ("🔮", "Predictor",      "توقع المغادرة", "pages/02_🔮_predictor.py"),
    ("📈", "Model Insights", "رؤى الموديل",   "pages/03_📈_insights.py"),
]


def spider():
    """
    ضيفي في أول كل صفحة:
        from spider import spider
        spider()
    """

    # ── Init session state ─────────────────────────────────────────
    if "theme" not in st.session_state: st.session_state.theme = "dark"
    if "lang"  not in st.session_state: st.session_state.lang  = "en"

    THEME = st.session_state.theme
    LANG  = st.session_state.lang

    # ── Palette ────────────────────────────────────────────────────
    if THEME == "dark":
        NAV_BG  = "#0a0e1a"
        NAV_BG2 = "#0f172a"
        ACCENT  = "#00d4ff"
        WHITE   = "#f1f5f9"
        GREY    = "#64748b"
        BORDER  = "rgba(0,212,255,0.13)"
        BTN_HV  = "rgba(0,212,255,0.14)"
        TGL_BG  = "rgba(255,255,255,0.05)"
        ICON_BG = "rgba(0,212,255,0.08)"
        ICON_HV = "rgba(0,212,255,0.20)"
        APP_BG  = "#07090f"
    else:
        NAV_BG  = "#f0f6ff"
        NAV_BG2 = "#e8f0fe"
        ACCENT  = "#0369a1"
        WHITE   = "#0f172a"
        GREY    = "#64748b"
        BORDER  = "rgba(3,105,161,0.15)"
        BTN_HV  = "rgba(3,105,161,0.12)"
        TGL_BG  = "rgba(0,0,0,0.05)"
        ICON_BG = "rgba(3,105,161,0.08)"
        ICON_HV = "rgba(3,105,161,0.20)"
        APP_BG  = "#f0f6ff"

    FF = "Tajawal" if LANG == "ar" else "Syne"

    # ── CSS ────────────────────────────────────────────────────────
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@400;500&family=Tajawal:wght@400;700;800&display=swap');

    /* ── App background ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {APP_BG} !important;
        color: {WHITE} !important;
    }}

    /* ── Sidebar always visible + hide collapse arrow ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAV_BG} 0%, {NAV_BG2} 100%) !important;
        border-right: 1px solid {BORDER} !important;
        min-width: 240px !important;
        display: flex !important;
        visibility: visible !important;
        transform: none !important;
        transition: none !important;
    }}
    /* إخفاء زرار السهم اللي بيطوي الـ sidebar */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    button[kind="headerNoPadding"],
    [data-testid="collapsedControl"] {{
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }}
    /* منع الـ sidebar من الاختفاء */
    [data-testid="stSidebar"][aria-expanded="false"] {{
        margin-left: 0 !important;
        display: flex !important;
        visibility: visible !important;
        min-width: 240px !important;
    }}
    [data-testid="stSidebarNav"]    {{ display: none !important; }}
    [data-testid="stSidebar"] *     {{ color: {WHITE} !important;
                                       font-family: '{FF}', sans-serif !important; }}

    /* ── All sidebar buttons reset ── */
    [data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: 1px solid transparent !important;
        color: {GREY} !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-size: .83rem !important;
        font-weight: 600 !important;
        padding: 9px 12px !important;
        margin-bottom: 2px !important;
        transition: all .18s ease !important;
        font-family: '{FF}', sans-serif !important;
        text-align: left !important;
        cursor: pointer !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: {BTN_HV} !important;
        color: {ACCENT} !important;
        border-color: {BORDER} !important;
    }}

    /* ── Nav icon buttons ── */
    .nav-icon-btn .stButton > button {{
        background: {ICON_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {WHITE} !important;
        border-radius: 12px !important;
        padding: 11px 14px !important;
        margin-bottom: 5px !important;
        font-size: .84rem !important;
        font-weight: 700 !important;
        text-align: left !important;
        transition: all .2s ease !important;
    }}
    .nav-icon-btn .stButton > button:hover {{
        background: {ICON_HV} !important;
        border-color: {ACCENT} !important;
        color: {ACCENT} !important;
        transform: translateX(4px) !important;
        box-shadow: 0 0 14px {BORDER} !important;
    }}

    /* ── Toggle buttons ── */
    .tgl-btn .stButton > button {{
        background: {TGL_BG} !important;
        border: 1px solid {BORDER} !important;
        color: {WHITE} !important;
        border-radius: 20px !important;
        padding: 6px 8px !important;
        font-size: .76rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }}
    .tgl-btn .stButton > button:hover {{
        background: {BTN_HV} !important;
        border-color: {ACCENT} !important;
        color: {ACCENT} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ── Sidebar Content ────────────────────────────────────────────
    with st.sidebar:

        # 1. Project Logo
        st.markdown(f"""
        <div style="text-align:center;padding:22px 10px 16px;
                    border-bottom:1px solid {BORDER}">
          <div style="width:58px;height:58px;border-radius:16px;
                      background:linear-gradient(135deg,#0f4c81,#00d4ff);
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 10px;font-size:26px;
                      box-shadow:0 4px 20px rgba(0,212,255,0.22)">🏦</div>
          <div style="font-family:'{FF}',sans-serif;font-weight:800;
                      font-size:12.5px;color:{WHITE};line-height:1.45;margin-bottom:4px">
            {'التنبؤ بمغادرة العملاء' if LANG=='ar' else 'Bank Customer<br>Churn Prediction'}
          </div>
          <div style="font-size:9.5px;color:{ACCENT};letter-spacing:1.3px;
                      text-transform:uppercase;font-weight:600">ML · Classification</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Profile
        st.markdown(f"""
        <div style="text-align:center;padding:15px 10px 13px;
                    border-bottom:1px solid {BORDER}">
          <div style="width:50px;height:50px;border-radius:50%;
                      background:linear-gradient(135deg,#00d4ff,#7c3aed);
                      display:flex;align-items:center;justify-content:center;
                      margin:0 auto 8px;font-size:20px;
                      box-shadow:0 0 14px rgba(0,212,255,0.22)">👩‍💻</div>
          <div style="font-family:'{FF}',sans-serif;font-weight:800;
                      font-size:13px;color:{WHITE};margin-bottom:2px">
            Eng. Shadya Dief
          </div>
          <div style="font-size:9px;color:{ACCENT};letter-spacing:1.3px;
                      text-transform:uppercase;font-weight:600;margin-bottom:11px">
            {'مهندسة تعلم الآلة' if LANG=='ar' else 'ML Engineer'}
          </div>
          <div style="display:flex;gap:6px;justify-content:center">
            <a href="https://www.linkedin.com/in/shadya-dief-ml/" target="_blank"
               style="padding:4px 10px;border-radius:20px;font-size:10px;font-weight:700;
                      text-decoration:none;background:rgba(10,102,194,0.15);
                      border:1px solid rgba(10,102,194,0.40);color:#60a5fa">
              in LinkedIn
            </a>
            <a href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
               target="_blank"
               style="padding:4px 10px;border-radius:20px;font-size:10px;font-weight:700;
                      text-decoration:none;background:{TGL_BG};
                      border:1px solid {BORDER};color:{WHITE}">
              ⌥ GitHub
            </a>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Theme + Lang toggles — rerun بس بعد ما نحفظ الـ state
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown('<div class="tgl-btn">', unsafe_allow_html=True)
            if st.button(
                "☀️ Light" if THEME == "dark" else "🌙 Dark",
                key="sp_theme", use_container_width=True
            ):
                st.session_state.theme = "light" if THEME == "dark" else "dark"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with tc2:
            st.markdown('<div class="tgl-btn">', unsafe_allow_html=True)
            if st.button(
                "🌐 عربي" if LANG == "en" else "🌐 English",
                key="sp_lang", use_container_width=True
            ):
                st.session_state.lang = "ar" if LANG == "en" else "en"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. Nav label
        st.markdown(f"""
        <div style="font-size:9px;font-weight:700;letter-spacing:1.8px;
                    text-transform:uppercase;color:{GREY};
                    padding:13px 2px 5px;opacity:0.65">
          📌 {'التنقل' if LANG=='ar' else 'Navigation'}
        </div>
        """, unsafe_allow_html=True)

        # 5. Nav buttons
        for icon, en_lbl, ar_lbl, fpath in NAV:
            label = f"{icon}  {ar_lbl}" if LANG == "ar" else f"{icon}  {en_lbl}"
            key   = "sp_" + os.path.basename(fpath).replace(" ", "_")
            st.markdown('<div class="nav-icon-btn">', unsafe_allow_html=True)
            if st.button(label, key=key, use_container_width=True):
                st.switch_page(fpath)
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. Footer
        st.markdown(f"""
        <div style="height:1px;background:{BORDER};margin:14px 0 10px"></div>
        <div style="font-size:.65rem;color:{GREY};text-align:center;line-height:1.9">
          Built with ❤️ by
          <a href="https://www.linkedin.com/in/shadya-dief-ml/" target="_blank"
             style="color:{ACCENT};text-decoration:none;font-weight:700">
            Eng. Shadya Dief
          </a>
        </div>
        """, unsafe_allow_html=True)

    return st.session_state.theme, st.session_state.lang
