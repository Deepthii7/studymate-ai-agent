from urllib import response

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def explainer_agent(topic):
    prompt = f"""
    Explain {topic} in a beginner-friendly way.

    Rules:
    - Maximum 200 words
    - Use simple language
    - Include one example
    - Use headings and bullet points
    - Keep the explanation concise
    """

    response = model.generate_content(prompt)
    return response.text


def quiz_agent(topic, explanation):
    prompt = f"""
    Based on this explanation:

    {explanation}

    Create exactly 3 quiz questions.

    Rules:
    - 1 Multiple Choice
    - 1 True/False
    - 1 Scenario-based question
    - Include answers
    - Keep explanations short

    Formatting rules (follow exactly):
    - For the Multiple Choice question, write each option on its own separate line,
      formatted exactly like:

      a) First option

      b) Second option

      c) Third option

      d) Fourth option

    - Do not place multiple options on the same line.
    - Never write "Answer:" on the same line as the question.
    - Leave one blank line before every "Answer:".
    """

    response = model.generate_content(prompt)
    return response.text


def planner_agent(topic,explanation):
    prompt = f"""
    Based on this explanation:

    {explanation}

    Create a concise 3-day study plan.

    Rules:
    - Day 1, Day 2, Day 3
    - Maximum 3 bullet points per day
    - Keep it practical and beginner-friendly
    """

    response = model.generate_content(prompt)
    return response.text


def generate_learning_package(topic):
    prompt = f"""
    Create a learning package about {topic}.

    Format exactly like this:

    ## EXPLANATION
    - Beginner-friendly explanation
    - Maximum 200 words
    - Include one example

    ## QUIZ

    - Create EXACTLY 3 questions.cv

    Question 1 (Multiple Choice)
    Options MUST be formatted exactly like:

    a) First option

    b) Second option

    c) Third option

    d) Fourth option

    Each option must be on its own separate line.
    Answer:

    ### Question 2 (True/False)
    Answer:

    ### Question 3 (Scenario-Based)
    - Ask the user to write a small code snippet or solve a practical problem
    Answer:
    - Provide the complete code solution

    IMPORTANT:
    - Every question must have its answer immediately below it
    - For multiple choice questions, use EXACTLY this format:

    a) Option A

    b) Option B

    c) Option C

    d) Option D

    Do not place multiple options on the same line.
    - Never write Answer: on the same line as the question
    - Leave one blank line before every Answer:
    - Do NOT place all answers at the end
    - Do NOT write options in a single paragraph

    ## STUDY PLAN
    - Day 1
    - Day 2
    - Day 3
    - Maximum 3 bullet points per day

    Keep everything concise.
    """

    response = model.generate_content(prompt)

    text = response.text

    text = text.replace(" a)", "\na)")
    text = text.replace(" b)", "\nb)")
    text = text.replace(" c)", "\nc)")
    text = text.replace(" d)", "\nd)")
    print(text)
    return text


# ============================================================
# COORDINATOR AGENT
# ------------------------------------------------------------
# Orchestrates the existing Explainer, Quiz Generator, and
# Study Planner agents instead of relying on one giant prompt.
#
# Flow:
#   1. explainer_agent(topic)              -> explanation
#   2. quiz_agent(topic, explanation)      -> quiz (uses explanation as context)
#   3. planner_agent(topic, explanation)   -> study plan (uses explanation as context)
#
# This keeps the total Gemini API calls at exactly 3 per
# "Generate Learning Package" click, while still being a real
# multi-agent pipeline (each agent has its own prompt/responsibility,
# and the Coordinator passes shared context between them).
#
# The final assembled string matches the exact section structure
# (## EXPLANATION / ### QUIZ / ## STUDY PLAN) that the UI already
# expects, so the on-screen output format does not change.
# ============================================================
def _strip_leading_indent(text):
    """
    Removes leading whitespace from every line in the given text.

    Why this is needed: Markdown (and therefore Streamlit's st.markdown)
    treats any line starting with 4+ spaces (or a tab) as an indented
    code block. Gemini sometimes echoes the indentation level used in
    the prompt's own example formatting (e.g. "    a) First option"),
    which would otherwise get rendered as a dark code block instead of
    plain text. This strips that leading whitespace without altering
    the actual content of each line.
    """
    return "\n".join(line.lstrip() for line in text.split("\n"))


def coordinator_agent(topic):
    # Step 1: Explainer Agent
    explanation = explainer_agent(topic)
    print("========== EXPLANATION ==========")
    print(repr(explanation))
    print("=================================")

    # Step 2: Quiz Generator Agent (grounded in the explanation)
    quiz = quiz_agent(topic, explanation)
    idx = quiz.find("a)")
    print("QUIZ SLICE:", repr(quiz[max(0, idx-60):idx+40]))

    # Step 3: Study Planner Agent (grounded in the explanation)
    study_plan = planner_agent(topic, explanation)

    # Strip any leading indentation Gemini may have echoed back, so
    # Streamlit never mistakes a line (e.g. "Answer:" or a code example)python3 -m pip show python-dotenv
    # for an indented Markdown code block.
    explanation = _strip_leading_indent(explanation)
    quiz = _strip_leading_indent(quiz)
    study_plan = _strip_leading_indent(study_plan)

    # Apply the same a)/b)/c)/d) line-break normalization used by
    # generate_learning_package(), since quiz_agent's output may not
    # always insert real newlines before each option.
    quiz = quiz.replace(" a)", "\na)")
    quiz = quiz.replace(" b)", "\nb)")
    quiz = quiz.replace(" c)", "\nc)")
    quiz = quiz.replace(" d)", "\nd)")

    # Assemble into the same overall format the app already renders.
    learning_package = f"""## EXPLANATION
{explanation}

### QUIZ
{quiz}

## STUDY PLAN
{study_plan}
"""

    print(learning_package)
    return learning_package

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="MindMesh AI",
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

html, body {
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
st.markdown("""
<style>
p, div, span {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# SCOPED FIX: restore Streamlit's default text color inside
# code blocks only. The global "p, div, span { color: black }"
# rule above (kept as-is) was also overriding the text color
# INSIDE Streamlit's dark-background code blocks, making text
# like "Answer:" nearly invisible (black text on a dark box).
#
# This rule is scoped to div[data-testid="stCodeBlock"] only,
# so it does not affect any other div/span/p elsewhere on the
# page (hero section, agent cards, feature cards, etc.).
# ------------------------------------------------------------
st.markdown("""
<style>
div[data-testid="stCodeBlock"] code,
div[data-testid="stCodeBlock"] span,
div[data-testid="stCodeBlock"] pre {
    color: #FAFAFA !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# BRAND BAR — minimal top nav, like a real SaaS product header
# ============================================================
st.markdown(
    """
    <div class="brand-bar">
        <div class="brand-logo">Mind<span>Mesh</span> AI</div>
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
        <div class="main-title">MindMesh AI</div>
        <div class="sub-title">Explain. Practice. Plan. Powered by collaborative AI agents.</div>
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
    MindMesh AI is a <b>multi-agent educational assistant</b> that coordinates a team of
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
        placeholder="Enter any topic and let your AI agents teach it",
        label_visibility="collapsed"
    )

    # Button to trigger the (future) multi-agent pipeline
    generate_clicked = st.button("Generate Learning Package")

    # Simple placeholder feedback when the button is clicked
if generate_clicked:
    if topic.strip() == "":
        st.warning("Please enter a topic before generating your learning package.")
    else:
        try:
            with st.spinner(" 🤖  Coordinator Agent is orchestrating your learning package..."):

                learning_package = coordinator_agent(topic)

                st.markdown(learning_package, unsafe_allow_html=True)

        except Exception as e:
            st.error(
                "⚠️ MindMesh AI is currently experiencing high demand. Please wait a minute and try again."
            )

            print(e)

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
st.markdown('<div class="section-header">What MindMesh AI does</div>', unsafe_allow_html=True)
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
    '<div class="footer-text">MindMesh AI • Multi-Agent Educational Assistant </div>',
    unsafe_allow_html=True
)