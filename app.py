import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS — MODERN SAAS THEME (WHITE + LAVENDER ACCENTS)
# ============================================================
custom_css = """
<style>
/* Import a clean, professional typeface pairing */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Dancing+Script:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Overall app background — pure white for a clean SaaS feel */
.stApp {
    background-color: #FFFFFF;
}

/* Hide Streamlit's default top padding for a tighter layout */
.block-container {
    padding-top: 2.5rem;
    max-width: 1100px;
}

/* ---------------- TOP NAV / BRAND BAR ---------------- */
.brand-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #EFEAF8;
    margin-bottom: 2.5rem;
}

.brand-logo {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1A1A2E;
    letter-spacing: -0.02em;
}

.brand-logo span {
    color: #8B7BC7;
}

.brand-tag {
    font-size: 0.8rem;
    color: #A39DBE;
    font-weight: 500;
    border: 1px solid #E9E2F7;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    background-color: #FAF8FE;
}

/* ---------------- HERO SECTION ---------------- */
.hero-wrap {
    text-align: center;
    margin-bottom: 2.2rem;
}

.hero-eyebrow {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #8B7BC7;
    background-color: #F4F0FC;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 1.2rem;
}

.main-title {
    font-family: "Dancing Script", cursive;
    color: #15141F;
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}

.sub-title {
    color: #6B6680;
    font-size: 1.1rem;
    font-weight: 400;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ---------------- DESCRIPTION CARD ---------------- */
.description-box {
    background-color: #FAF9FD;
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    color: #4D4A5E;
    font-size: 0.97rem;
    line-height: 1.65;
    border: 1px solid #EFEAF8;
    margin: 1.8rem 0 2.2rem 0;
    text-align: center;
}

.description-box b {
    color: #1A1A2E;
}

/* ---------------- INPUT SECTION ---------------- */
.input-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #3A374A;
    margin-bottom: 0.4rem;
}

div.stTextInput > div > div > input {
    border-radius: 10px;
    border: 1.5px solid #E7E1F5;
    padding: 0.7rem 0.9rem;
    font-size: 0.95rem;
    color: #1A1A2E;
    background-color: #FCFBFE;
}

div.stTextInput > div > div > input:focus {
    border-color: #B5A6E8;
    box-shadow: 0 0 0 3px rgba(181, 166, 232, 0.15);
}

div.stTextInput > div > div > input::placeholder {
    color: #B3AFC6;
}

/* Custom button — solid lavender, SaaS primary-action style */
div.stButton > button {
    background-color: #7C6BC4;
    color: #FFFFFF;
    font-weight: 600;
    font-size: 0.95rem;
    border-radius: 10px;
    padding: 0.65rem 1.5rem;
    border: none;
    width: 100%;
    letter-spacing: -0.01em;
    transition: background-color 0.15s ease-in-out, transform 0.1s ease-in-out;
}

div.stButton > button:hover {
    background-color: #6A58B8;
    transform: translateY(-1px);
}

div.stButton > button:active {
    transform: translateY(0px);
}

/* ---------------- SECTION HEADERS ---------------- */
.section-header {
    color: #15141F;
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-top: 3rem;
    margin-bottom: 0.3rem;
}

.section-subtext {
    color: #918CA3;
    font-size: 0.9rem;
    margin-bottom: 1.4rem;
}

/* ---------------- AGENT CARDS (compact) ---------------- */
.agent-card {
    background-color: #FFFFFF;
    border: 1px solid #EFEAF8;
    border-radius: 14px;
    padding: 1.1rem 1rem;
    height: 168px;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.agent-card:hover {
    border-color: #D9CDF2;
    box-shadow: 0 4px 14px rgba(124, 107, 196, 0.08);
}

.agent-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background-color: #F4F0FC;
    font-size: 1.05rem;
    margin-bottom: 0.65rem;
}

.agent-title {
    color: #1A1A2E;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
    letter-spacing: -0.01em;
}

.agent-desc {
    color: #837E97;
    font-size: 0.82rem;
    line-height: 1.45;
}

/* ---------------- FEATURE CARDS (compact, minimal) ---------------- */
.feature-card {
    background-color: #FAF9FD;
    border-radius: 12px;
    padding: 1rem 0.9rem;
    border: 1px solid #F1ECFA;
    height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.feature-text {
    color: #1A1A2E;
    font-weight: 600;
    font-size: 0.88rem;
    margin-bottom: 0.15rem;
}

.feature-subtext {
    color: #9B96AC;
    font-size: 0.74rem;
    line-height: 1.3;
}

/* ---------------- FOOTER ---------------- */
.footer-text {
    text-align: center;
    color: #C2BDD1;
    font-size: 0.78rem;
    margin-top: 3.5rem;
    padding: 1.2rem 0;
    border-top: 1px solid #F4F0FC;
}
</style>
"""

# Inject the custom CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================
# BRAND BAR — minimal top nav, like a real SaaS product header
# ============================================================
st.markdown(
    """
    <div class="brand-bar">
        <div class="brand-logo">Study<span>Mate</span> AI</div>
        <div class="brand-tag">Kaggle Capstone Project</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HERO SECTION — TITLE & SUBTITLE (centered, SaaS landing style)
# ============================================================
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-eyebrow">Multi-Agent Learning System</div>
        <div class="main-title">StudyMate AI</div>
        <div class="sub-title">Your AI-powered study companion — built to explain concepts,
        generate quizzes, and plan your learning, all in one place.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PROJECT DESCRIPTION SECTION
# ============================================================
st.markdown(
    """
    <div class="description-box">
    StudyMate AI is a <b>multi-agent educational assistant</b> that coordinates a team of
    specialized AI agents to help you learn more efficiently. One agent explains concepts in
    plain language, another builds quizzes to test your understanding, and another designs a
    study plan around your goals. Enter a topic below to get started.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# TOPIC INPUT & GENERATE BUTTON SECTION
# ============================================================
# Center the input and button using a column layout
input_col1, input_col2, input_col3 = st.columns([1, 2.2, 1])

with input_col2:
    st.markdown('<div class="input-label">Enter a topic you want to learn</div>', unsafe_allow_html=True)

    # Text input for the topic the student wants to learn
    topic = st.text_input(
        label="Enter a topic you want to learn",
        placeholder="e.g. Newton's Laws of Motion",
        label_visibility="collapsed"
    )

    # Button to trigger the (future) multi-agent pipeline
    generate_clicked = st.button("Generate Learning Package")

    # Simple placeholder feedback when the button is clicked
if generate_clicked:
    if topic.strip() == "":
        st.warning("Please enter a topic before generating your learning package.")
    else:
        response = model.generate_content(topic)
        st.write(response.text)

# ============================================================
# "MEET YOUR AI AGENTS" SECTION
# ============================================================
st.markdown('<div class="section-header">Meet your AI agents</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtext">Each agent specializes in one part of how you learn.</div>', unsafe_allow_html=True)

# Create four columns, one for each agent card
agent_col1, agent_col2, agent_col3, agent_col4 = st.columns(4)

# Coordinator Agent Card
with agent_col1:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-badge">🎯</div>
            <div class="agent-title">Coordinator</div>
            <div class="agent-desc">Routes your request to the right agent for the job.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Explainer Agent Card
with agent_col2:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-badge">📖</div>
            <div class="agent-title">Explainer</div>
            <div class="agent-desc">Breaks down concepts with simple, clear examples.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Quiz Agent Card
with agent_col3:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-badge">📝</div>
            <div class="agent-title">Quiz Generator</div>
            <div class="agent-desc">Builds quizzes and practice questions to test recall.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Study Planner Agent Card
with agent_col4:
    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-badge">📅</div>
            <div class="agent-title">Study Planner</div>
            <div class="agent-desc">Maps out a learning roadmap and study schedule.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# "FEATURES" SECTION
# ============================================================
st.markdown('<div class="section-header">What StudyMate AI does</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtext">A focused toolset, not a bloated one.</div>', unsafe_allow_html=True)

# Create four columns, one for each feature highlight
feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

with feature_col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-text">Concept Explanations</div>
            <div class="feature-subtext">Clear, beginner-friendly breakdowns of any topic.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature_col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-text">Quiz Generation</div>
            <div class="feature-subtext">Practice questions that target what you just learned.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature_col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-text">Personalized Plans</div>
            <div class="feature-subtext">Study schedules shaped around your pace and goals.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature_col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-text">Multi-Agent Architecture</div>
            <div class="feature-subtext">Specialized agents working together behind one interface.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER SECTION
# ============================================================
st.markdown(
    '<div class="footer-text">StudyMate AI • Multi-Agent Educational Assistant </div>',
    unsafe_allow_html=True
)
