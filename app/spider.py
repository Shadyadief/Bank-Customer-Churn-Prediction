import streamlit as st


# ── Translations Dictionary ────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "project_name":    "Bank Customer\nChurn Prediction",
        "project_sub":     "ML · Classification",
        "profile_title":   "ML Engineer",
        "nav_label":       "📌 Navigation",
        "lang_btn":        "🌐 عربي",
        "theme_dark":      "🌙 Dark",
        "theme_light":     "☀️ Light",
    },
    "ar": {
        "project_name":    "التنبؤ بمغادرة\nعملاء البنك",
        "project_sub":     "تعلم الآلة · تصنيف",
        "profile_title":   "مهندسة تعلم الآلة",
        "nav_label":       "📌 التنقل",
        "lang_btn":        "🌐 English",
        "theme_dark":      "🌙 داكن",
        "theme_light":     "☀️ فاتح",
    },
}

# ── Theme Palettes ─────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "--bg-sidebar":       "linear-gradient(180deg, #0f172a 0%, #0a0e1a 100%)",
        "--bg-base":          "#07090f",
        "--bg-card":          "#111827",
        "--text-primary":     "#f1f5f9",
        "--text-muted":       "#94a3b8",
        "--accent":           "#00d4ff",
        "--border":           "rgba(0,212,255,0.14)",
        "--btn-lang-bg":      "rgba(0,212,255,0.10)",
        "--btn-lang-border":  "rgba(0,212,255,0.35)",
        "--btn-lang-color":   "#00d4ff",
        "--btn-theme-bg":     "rgba(255,255,255,0.06)",
        "--btn-theme-border": "rgba(255,255,255,0.18)",
        "--btn-theme-color":  "#e2e8f0",
        "--divider":          "rgba(0,212,255,0.10)",
    },
    "light": {
        "--bg-sidebar":       "linear-gradient(180deg, #f0f6ff 0%, #e8f0fe 100%)",
        "--bg-base":          "#f8fafc",
        "--bg-card":          "#ffffff",
        "--text-primary":     "#0f172a",
        "--text-muted":       "#475569",
        "--accent":           "#0369a1",
        "--border":           "rgba(3,105,161,0.18)",
        "--btn-lang-bg":      "rgba(3,105,161,0.08)",
        "--btn-lang-border":  "rgba(3,105,161,0.35)",
        "--btn-lang-color":   "#0369a1",
        "--btn-theme-bg":     "rgba(0,0,0,0.05)",
        "--btn-theme-border": "rgba(0,0,0,0.15)",
        "--btn-theme-color":  "#1e293b",
        "--divider":          "rgba(3,105,161,0.12)",
    },
}


def spider():
    """
    ضيفي في أول كل صفحة سطرين بس:

        from spider import spider
        spider()

    Session state تلقائياً:
        st.session_state.lang   →  'en' | 'ar'
        st.session_state.theme  →  'dark' | 'light'
    """

    # ── Init session state ────────────────────────────────────────────────────
    if "lang"  not in st.session_state: st.session_state.lang  = "en"
    if "theme" not in st.session_state: st.session_state.theme = "dark"

    lang  = st.session_state.lang
    theme = st.session_state.theme
    t     = TRANSLATIONS[lang]
    p     = THEMES[theme]

    # ── CSS Variables from active theme ───────────────────────────────────────
    css_vars = "\n".join([f"        {k}: {v};" for k, v in p.items()])

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Mono:wght@400;500&display=swap');

    :root {{
        {css_vars}
    }}

    /* ── App background ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--divider) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: var(--text-primary) !important;
    }}

    /* ── Project Logo block ── */
    .project-top {{
        text-align: center;
        padding: 22px 14px 18px;
        border-bottom: 1px solid var(--divider);
    }}
    .project-logo {{
        width: 62px; height: 62px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f4c81 0%, #00d4ff 100%);
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 11px;
        font-size: 28px;
        box-shadow: 0 4px 20px rgba(0,212,255,0.22);
    }}
    .project-name {{
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 13px;
        color: var(--text-primary);
        line-height: 1.45;
        margin-bottom: 5px;
        white-space: pre-line;
    }}
    .project-subtitle {{
        font-size: 10px;
        color: var(--accent);
        letter-spacing: 1.3px;
        text-transform: uppercase;
        font-weight: 600;
    }}

    /* ── Profile block ── */
    .profile-card {{
        text-align: center;
        padding: 18px 14px 16px;
        border-bottom: 1px solid var(--divider);
    }}
    .avatar-ring {{
        width: 58px; height: 58px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 9px;
        font-size: 24px;
        box-shadow: 0 0 16px rgba(0,212,255,0.25);
    }}
    .profile-name {{
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 14px;
        color: var(--text-primary);
        margin-bottom: 3px;
    }}
    .profile-title {{
        font-size: 10px;
        color: var(--accent);
        letter-spacing: 1.3px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 13px;
    }}
    .social-row {{
        display: flex; gap: 8px; justify-content: center;
    }}
    .social-btn {{
        display: flex; align-items: center; gap: 5px;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }}
    .btn-linkedin {{
        background: rgba(10,102,194,0.15);
        border: 1px solid rgba(10,102,194,0.40);
        color: #60a5fa !important;
    }}
    .btn-linkedin:hover {{
        background: rgba(10,102,194,0.30);
        box-shadow: 0 0 10px rgba(10,102,194,0.30);
    }}
    .btn-github {{
        background: var(--btn-theme-bg);
        border: 1px solid var(--btn-theme-border);
        color: var(--btn-theme-color) !important;
    }}
    .btn-github:hover {{
        background: rgba(255,255,255,0.12);
    }}

    /* ── Toggle buttons row ── */
    .toggle-row {{
        display: flex; gap: 8px;
        padding: 14px 14px 4px;
        justify-content: center;
    }}
    .toggle-btn {{
        flex: 1;
        padding: 6px 0;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
        border: none;
        font-family: 'DM Mono', monospace;
    }}
    .btn-lang {{
        background: var(--btn-lang-bg);
        border: 1px solid var(--btn-lang-border) !important;
        color: var(--btn-lang-color);
    }}
    .btn-theme {{
        background: var(--btn-theme-bg);
        border: 1px solid var(--btn-theme-border) !important;
        color: var(--btn-theme-color);
    }}

    /* ── Nav label ── */
    .nav-label {{
        font-size: 9.5px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: var(--text-muted);
        padding: 14px 16px 5px;
        opacity: 0.6;
    }}

    /* ── Streamlit button override for toggles ── */
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        border-radius: 20px !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        padding: 6px 8px !important;
        transition: all 0.2s ease !important;
        border: 1px solid var(--border) !important;
        background: var(--btn-lang-bg) !important;
        color: var(--accent) !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 10px var(--accent) !important;
        opacity: 0.9;
    }}
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:

        # ── 1. Project Logo + Name ───────────────────────────────────────────
        proj_lines = t["project_name"].split("\n")
        st.markdown(f"""
        <div class="project-top">
            <div class="project-logo">🏦</div>
            <div class="project-name">{proj_lines[0]}<br>{proj_lines[1]}</div>
            <div class="project-subtitle">{t["project_sub"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. Profile + Social Links ────────────────────────────────────────
        st.markdown(f"""
        <div class="profile-card">
            <div class="avatar-ring">👩‍💻</div>
            <div class="profile-name">Eng. Shadya Dief</div>
            <div class="profile-title">{t["profile_title"]}</div>
            <div class="social-row">
                <a class="social-btn btn-linkedin"
                   href="https://www.linkedin.com/in/shadya-dief-ml/"
                   target="_blank">in LinkedIn</a>
                <a class="social-btn btn-github"
                   href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
                   target="_blank">⌥ GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3. Language + Theme toggles ──────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            if st.button(t["lang_btn"], key="toggle_lang", use_container_width=True):
                st.session_state.lang = "ar" if lang == "en" else "en"
                st.rerun()
        with col2:
            theme_label = t["theme_light"] if theme == "dark" else t["theme_dark"]
            if st.button(theme_label, key="toggle_theme", use_container_width=True):
                st.session_state.theme = "light" if theme == "dark" else "dark"
                st.rerun()

        # ── 4. Navigation Label ──────────────────────────────────────────────
        st.markdown(f'<div class="nav-label">{t["nav_label"]}</div>', unsafe_allow_html=True)
