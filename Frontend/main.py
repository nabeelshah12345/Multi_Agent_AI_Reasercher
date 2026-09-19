
import streamlit as st
import requests

API_URL = "https://multi-agent-ai-research-nabeelshah12345s-projects.vercel.app"   # FastAPI jahan run ho raha hai
REQUEST_TIMEOUT_SECONDS = 90


def post_api(path, payload):
    """Call the backend and surface its actual error message in the UI."""
    response = requests.post(
        f"{API_URL}{path}",
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = response.text[:300]
        raise RuntimeError(detail or f"Backend request failed ({response.status_code}).") from exc

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError("The backend returned an invalid response.") from exc

st.set_page_config(page_title="BrainForge", layout="wide", page_icon="🧠")


st.markdown("""
<style>
    .stApp {
        background-color: #0e0e10;
        color: #e8e8e8;
    }

    /* ---- Hero Section ---- */
    .hero-eyebrow {
        color: #ff9d3a;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 3px;
        text-align: center;
        margin-bottom: 8px;
    }
    .hero-title {
        text-align: center;
        font-size: 64px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    .hero-title .brain { color: #f5f1ea; }
    .hero-title .forge { color: #ff9d3a; }
   

    /* ---- Input & Button ---- */
    .stTextInput input {
        background-color: #1a1a1d;
        color: #ffffff;
        border: 1px solid #2e2e33;
        border-radius: 8px;
        padding: 12px;
        font-size: 15px;
    }
    .stButton button {
        background: linear-gradient(90deg, #ff7a18, #ff9d3a);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #ff8a2e, #ffad4a);
        color: white;
    }

    /* ---- Pipeline Cards ---- */
    .pipeline-card {
        background-color: #17171a;
        border-left: 3px solid #3a3a3f;
        border-radius: 6px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .pipeline-card.done { border-left: 3px solid #3ddc84; }
    .pipeline-card.running { border-left: 3px solid #ff9d3a; }
    .pipeline-step-num {
        color: #ff9d3a;
        font-weight: 700;
        font-size: 13px;
    }
    .pipeline-step-title {
        font-weight: 700;
        font-size: 16px;
        color: #ffffff;
    }
    .pipeline-step-desc {
        color: #9a9a9f;
        font-size: 13px;
        margin-top: 2px;
    }
    .badge-done { color: #3ddc84; font-weight: 700; font-size: 12px; float: right; }
    .badge-running { color: #ff9d3a; font-weight: 700; font-size: 12px; float: right; }
    .badge-pending { color: #5a5a5f; font-weight: 700; font-size: 12px; float: right; }

    /* ---- Final Report Container ---- */
    .report-container {
        background-color: #17171a;
        border: 1px solid #2e2e33;
        border-radius: 12px;
        padding: 32px;
        margin-top: 24px;
    }
    .report-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        border-bottom: 1px solid #2e2e33;
        padding-bottom: 16px;
    }
    .score-badge {
        display: inline-block;
        background: linear-gradient(90deg, #ff7a18, #ff9d3a);
        color: white;
        font-weight: 700;
        font-size: 15px;
        padding: 6px 16px;
        border-radius: 20px;
    }
    .feedback-box {
        background-color: #1a1a1d;
        border-left: 3px solid #ff9d3a;
        border-radius: 6px;
        padding: 16px;
        margin-top: 16px;
        color: #c9c9cd;
        font-size: 14px;
   
    }

    h1, h2, h3 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)


# ---- HERO ----
st.markdown("""
<div class="hero-eyebrow">MULTI-AGENT AI SYSTEM</div>
<div class="hero-title"><span class="brain">Brain</span><span class="forge">Forge</span></div>

""", unsafe_allow_html=True)


def render_step(placeholder, number, title, desc, status):
    css_class = "done" if status == "done" else ("running" if status == "running" else "")
    badge_text = "✓ DONE" if status == "done" else ("⏳ RUNNING" if status == "running" else "PENDING")

    placeholder.markdown(f"""
    <div class="pipeline-card {css_class}">
        <span class="pipeline-step-num">{number}</span>
        <span class="badge-{status}">{badge_text}</span><br>
        <span class="pipeline-step-title">{title}</span>
        <div class="pipeline-step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### RESEARCH TOPIC")
    topic = st.text_input("", placeholder="e.g. Quantum computing breakthroughs in 2025", label_visibility="collapsed")
    run_clicked = st.button("⚡ Run Research Pipeline")

with col2:
    st.markdown("#### Pipeline")
    step1 = st.empty()
    step2 = st.empty()
    step3 = st.empty()
    step4 = st.empty()

render_step(step1, "01", "Search Agent", "Gathers recent web information", "pending")
render_step(step2, "02", "Reader Agent", "Scrapes & extracts deep content", "pending")
render_step(step3, "03", "Writer Chain", "Drafts the full research report", "pending")
render_step(step4, "04", "Critic Chain", "Reviews & scores the report", "pending")

# Session state mein report/score store karo taake "Refine" button click hone par
if "report" not in st.session_state:
    st.session_state.report = None
    st.session_state.feedback = None
    st.session_state.score = None


# Real API calls jab "Run Research Pipeline" button click ho
if run_clicked and topic:
    try:
        render_step(step1, "01", "Search Agent", "Gathers recent web information", "running")
        r1 = post_api("/search", {"topic": topic})
        search_result = r1["search_result"]
        render_step(step1, "01", "Search Agent", "Gathers recent web information", "done")

        render_step(step2, "02", "Reader Agent", "Scrapes & extracts deep content", "running")
        r2 = post_api("/read", {"topic": topic, "search_result": search_result})
        scraped_result = r2["scraped_result"]
        render_step(step2, "02", "Reader Agent", "Scrapes & extracts deep content", "done")

        render_step(step3, "03", "Writer Chain", "Drafts the full research report", "running")
        r3 = post_api("/write", {
            "topic": topic,
            "search_result": search_result,
            "scraped_result": scraped_result,
        })
        report = r3["report"]
        render_step(step3, "03", "Writer Chain", "Drafts the full research report", "done")

        render_step(step4, "04", "Critic Chain", "Reviews & scores the report", "running")
        r4 = post_api("/score", {"report": report})
        render_step(step4, "04", "Critic Chain", "Reviews & scores the report", "done")

        # Results ko session_state mein save karo
        st.session_state.report = report
        st.session_state.feedback = r4["feedback"]
        st.session_state.score = r4["score"]

    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower() or "429" in error_msg:
            st.error("⚠️ Rate limit reached — please try again after 10-15 minutes.")
        else:
            st.error(f"⚠️ Something went wrong: {error_msg}")

# ---- Results display (session_state se, taake button clicks pe bhi persist rahe) ----
if st.session_state.report:
    st.markdown('<div class="report-container">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="report-header">
        <h2 style="margin:0;">📄 Final Report</h2>
        <span class="score-badge">Score: {st.session_state.score}/10</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(st.session_state.report)

    st.markdown(f'<div class="feedback-box">{st.session_state.feedback}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Report",
        data=st.session_state.report,
        file_name=f"{topic.replace(' ', '_')}_report.md",
        mime="text/markdown"
    )

    if st.session_state.score and st.session_state.score < 7:
        if st.button("🔁 Refine Report"):
            try:
                r5 = post_api("/refine", {
                    "report": st.session_state.report,
                    "feedback": st.session_state.feedback
                })
                refined = r5["refined_report"]

                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown('<h2 style="margin:0;">✨ Refined Report</h2>', unsafe_allow_html=True)
                st.markdown(refined)
                st.markdown('</div>', unsafe_allow_html=True)

                st.download_button(
                    label="⬇️ Download Refined Report",
                    data=refined,
                    file_name=f"{topic.replace(' ', '_')}_refined_report.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"⚠️ Refine failed: {str(e)}")
