import streamlit as st


def spider():
    """
    ضيفي في أول كل صفحة سطرين بس:

        from spider import spider
        spider()
    """

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&display=swap');

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0a0e1a 100%) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.12) !important;
    }

    /* ── Project Logo Section ── */
    .project-top {
        text-align: center;
        padding: 24px 16px 20px;
        border-bottom: 1px solid rgba(0, 212, 255, 0.12);
    }
    .project-logo {
        width: 64px; height: 64px;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f4c81 0%, #00d4ff 100%);
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px;
        font-size: 30px;
        box-shadow: 0 4px 20px rgba(0,212,255,0.25);
    }
    .project-name {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 13.5px;
        color: #f1f5f9;
        letter-spacing: 0.4px;
        line-height: 1.4;
        margin-bottom: 4px;
    }
    .project-subtitle {
        font-size: 10.5px;
        color: rgba(0, 212, 255, 0.75);
        letter-spacing: 1.2px;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* ── Profile Section ── */
    .profile-card {
        text-align: center;
        padding: 20px 16px 18px;
        border-bottom: 1px solid rgba(0, 212, 255, 0.08);
    }
    .avatar-ring {
        width: 62px; height: 62px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 10px;
        font-size: 26px;
        box-shadow: 0 0 18px rgba(0,212,255,0.28);
    }
    .profile-name {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 15px;
        color: #f1f5f9;
        letter-spacing: 0.3px;
        margin-bottom: 3px;
    }
    .profile-title {
        font-size: 10.5px;
        color: #00d4ff;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 14px;
    }

    /* ── Social Buttons ── */
    .social-row {
        display: flex;
        gap: 8px;
        justify-content: center;
    }
    .social-btn {
        display: flex; align-items: center; gap: 6px;
        padding: 6px 13px;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 600;
        text-decoration: none !important;
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
    }
    .btn-linkedin {
        background: rgba(10,102,194,0.18);
        border: 1px solid rgba(10,102,194,0.45);
        color: #60a5fa !important;
    }
    .btn-linkedin:hover {
        background: rgba(10,102,194,0.35);
        box-shadow: 0 0 12px rgba(10,102,194,0.35);
        color: #93c5fd !important;
    }
    .btn-github {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.18);
        color: #e2e8f0 !important;
    }
    .btn-github:hover {
        background: rgba(255,255,255,0.13);
        box-shadow: 0 0 12px rgba(255,255,255,0.1);
        color: #fff !important;
    }

    /* ── Nav Label ── */
    .nav-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: rgba(148,163,184,0.45);
        padding: 16px 18px 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:

        # ── 1. Project Logo + Name ──────────────────────────
        st.markdown("""
        <div class="project-top">
            <div class="project-logo">🏦</div>
            <div class="project-name">Bank Customer<br>Churn Prediction</div>
            <div class="project-subtitle">ML · Classification</div>
        </div>
        """, unsafe_allow_html=True)

        # ── 2. Profile + Social Links ───────────────────────
        st.markdown("""
        <div class="profile-card">
            <div class="avatar-ring">👩‍💻</div>
            <div class="profile-name">Eng. Shadya Dief</div>
            <div class="profile-title">ML Engineer</div>
            <div class="social-row">
                <a class="social-btn btn-linkedin"
                   href="https://www.linkedin.com/in/shadya-dief-ml/"
                   target="_blank">
                   <span>in</span> LinkedIn
                </a>
                <a class="social-btn btn-github"
                   href="https://github.com/Shadyadief/Bank-Customer-Churn-Prediction"
                   target="_blank">
                   <span>⌥</span> GitHub
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3. Navigation Label ─────────────────────────────
        st.markdown('<div class="nav-label">📌 Navigation</div>', unsafe_allow_html=True)
