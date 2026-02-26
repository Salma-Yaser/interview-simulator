import streamlit as st
from groq import Groq
from fpdf import FPDF
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Interview Simulator", page_icon="◈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg:         #0e1117;
    --bg-card:    #161b27;
    --bg-raised:  #1c2333;
    --bg-input:   #1a2035;
    --border:     #2a3347;
    --border-hi:  #354060;
    --text:       #e8edf5;
    --soft:       #b0bcd4;
    --muted:      #6b7a99;
    --dim:        #3d4f6e;
    --sky:        #5b9cf6;
    --sky-light:  #93bfff;
    --sky-dim:    rgba(91,156,246,0.12);
    --sky-glow:   rgba(91,156,246,0.2);
    --mauve:      #b89cf7;
    --teal:       #5ec4b8;
    --teal-dim:   rgba(94,196,184,0.1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 60% 40% at 90% 5%, rgba(91,156,246,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 40% 35% at 5% 95%, rgba(184,156,247,0.05) 0%, transparent 55%),
        #0e1117 !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { display: none !important; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* gap on both sides */
[data-testid="stHorizontalBlock"] {
    padding: 0 1.5rem !important;
    gap: 2rem !important;
}

/* ══════════════════════════════════
   FIXED LEFT PANEL
══════════════════════════════════ */
.layout-wrapper {
    display: flex;
    height: 100vh;
    overflow: hidden;
}

.left-panel {
    width: 360px;
    min-width: 360px;
    height: 100vh;
    overflow-y: auto;
    background: var(--bg-card);
    border-right: 1px solid var(--border);
    padding: 2.5rem 2rem 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 0;
    position: fixed;
    left: 0; top: 0;
}

.right-panel {
    margin-left: 360px;
    flex: 1;
    height: 100vh;
    overflow-y: auto;
    padding: 2.5rem 3rem 2.5rem 2rem;
}

/* ── Logo ── */
LOGO_PLACEHOLDER {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 2.2rem; padding-bottom: 1.8rem;
    border-bottom: 1px solid var(--border);
}
.logo-box {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, var(--sky), var(--mauve));
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Fira Code', monospace;
    font-size: 13px; font-weight: 500; color: #fff;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(91,156,246,0.3);
}
.logo-title {
    font-size: 0.875rem; font-weight: 600;
    color: var(--text); line-height: 1.2;
}
.logo-sub {
    font-family: 'Fira Code', monospace;
    font-size: 0.58rem; color: var(--muted); letter-spacing: 0.06em;
}

/* ── Section label ── */
.section-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.58rem; font-weight: 500;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--dim); margin-bottom: 1.2rem;
}

/* ── Labels ── */
label, .stSelectbox label, .stMultiSelect label, .stSlider label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.6rem !important; font-weight: 500 !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Inputs ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 9px !important;
    color: var(--text) !important;
    font-size: 0.875rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stMultiSelect"] > div > div:hover {
    border-color: var(--sky) !important;
    box-shadow: 0 0 0 3px rgba(91,156,246,0.1) !important;
}

/* ── Multiselect tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: var(--sky-dim) !important;
    border: 1px solid rgba(91,156,246,0.3) !important;
    border-radius: 6px !important;
    color: var(--sky-light) !important;
    font-size: 0.7rem !important;
    font-family: 'Fira Code', monospace !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] svg { fill: var(--sky-light) !important; }

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div { background: var(--sky) !important; }
[data-testid="stSlider"] [role="slider"] {
    background: var(--bg-card) !important;
    border: 2px solid var(--sky) !important;
    box-shadow: 0 0 10px rgba(91,156,246,0.5) !important;
}
[data-testid="stSlider"] > div > div > div { background: var(--border-hi) !important; }

/* ── Generate Button ── */
.stButton > button {
    background: #4a72c4 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 0.78rem !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
    padding: 0.8rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(74,114,196,0.3) !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #5580d4 !important;
    box-shadow: 0 6px 24px rgba(74,114,196,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border-hi) !important;
    color: var(--soft) !important; border-radius: 9px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.75rem !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    padding: 0.7rem 1.4rem !important; transition: all 0.2s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: var(--sky-dim) !important;
    border-color: var(--sky) !important;
    color: var(--sky-light) !important;
}

/* ══════════════════════════════════
   RIGHT PANEL CONTENT
══════════════════════════════════ */

/* ── Hero ── */
.hero { margin-bottom: 2.5rem; }
.hero-eyebrow {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--sky); margin-bottom: 0.8rem; opacity: 0.8;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before {
    content: ''; width: 16px; height: 1px;
    background: var(--sky); opacity: 0.6;
}
.hero-title {
    font-size: 2.2rem; font-weight: 700;
    letter-spacing: -0.03em; margin-bottom: 0.7rem; line-height: 1.15;
    background: linear-gradient(125deg, var(--text) 30%, var(--sky-light) 65%, var(--mauve) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc { font-size: 0.875rem; color: var(--muted); font-weight: 300; line-height: 1.8; }
.hero-line {
    height: 1px; margin-top: 2rem;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── Empty state ── */
.empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; text-align: center;
    padding: 5rem 2rem; margin-top: 1rem;
    border: 1px dashed var(--border-hi); border-radius: 16px;
    background: linear-gradient(135deg, rgba(91,156,246,0.02), transparent);
}
.empty-icon {
    font-family: 'Fira Code', monospace; font-size: 1.5rem;
    color: var(--dim); margin-bottom: 1.2rem;
}
.empty-text {
    font-family: 'Fira Code', monospace; font-size: 0.7rem;
    color: var(--muted); letter-spacing: 0.05em; line-height: 1.9;
}

/* ── Results meta ── */
.results-meta {
    background: var(--bg-card); border: 1px solid var(--border-hi);
    border-radius: 12px; padding: 1.2rem 1.6rem;
    margin-bottom: 1.5rem; position: relative; overflow: hidden;
}
.results-meta::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--sky), var(--mauve));
    opacity: 0.7;
}
.meta-role { font-size: 0.975rem; font-weight: 600; color: var(--text); margin-bottom: 0.2rem; }
.meta-sub {
    font-family: 'Fira Code', monospace; font-size: 0.63rem;
    color: var(--muted); margin-bottom: 0.8rem; letter-spacing: 0.04em;
}
.tag {
    display: inline-block;
    background: var(--sky-dim); border: 1px solid rgba(91,156,246,0.25);
    border-radius: 5px; padding: 0.15rem 0.5rem;
    font-family: 'Fira Code', monospace; font-size: 0.62rem;
    color: var(--sky-light); margin-right: 0.3rem; margin-bottom: 0.3rem;
}

/* ── Q Cards ── */
.q-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 0.7rem;
    transition: border-color 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}
.q-card:hover {
    border-color: var(--border-hi);
    transform: translateX(3px);
    box-shadow: -3px 0 20px rgba(91,156,246,0.06);
}
.q-badge {
    font-family: 'Fira Code', monospace; font-size: 0.58rem;
    color: var(--sky-light); letter-spacing: 0.12em; text-transform: uppercase;
    background: var(--sky-dim); border: 1px solid rgba(91,156,246,0.2);
    border-radius: 4px; padding: 0.18rem 0.5rem;
    display: inline-block; margin-bottom: 0.75rem;
}
.q-text {
    font-size: 0.9rem; font-weight: 500; color: var(--text);
    line-height: 1.65; margin-bottom: 1rem;
}
.a-row {
    display: flex; align-items: flex-start; gap: 0.7rem;
    padding-top: 0.9rem; border-top: 1px solid var(--border);
}
.a-badge {
    font-family: 'Fira Code', monospace; font-size: 0.56rem;
    color: var(--teal); letter-spacing: 0.1em; text-transform: uppercase;
    background: var(--teal-dim); border: 1px solid rgba(94,196,184,0.2);
    border-radius: 4px; padding: 0.18rem 0.4rem; flex-shrink: 0; margin-top: 2px;
}
.a-text { font-size: 0.855rem; color: var(--soft); line-height: 1.72; font-weight: 300; }

/* ── Export row ── */
.export-row { margin-top: 0; padding-top: 1rem; border-top: 1px solid var(--border); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════
# FUNCTIONS
# ══════════════════════════════════
def generate_questions(role, topics, level, round_type, num_questions):
    client = Groq(api_key=API_KEY)
    prompt = f"""You are an expert technical interviewer.
Generate exactly {num_questions} interview questions with answers for:
- Role: {role}
- Topics: {', '.join(topics)}
- Experience Level: {level}
- Round Type: {round_type}

Format EXACTLY like this:
Q1: [question]
A1: [concise 1-2 line answer]

Q2: [question]
A2: [concise 1-2 line answer]

Rules: specific, role-relevant, factually correct, vary difficulty by level.
"""
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=2000,
    )
    return r.choices[0].message.content


def parse_qa(text):
    qa_list, current_q = [], None
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('Q') and ':' in line:
            current_q = line.split(':', 1)[1].strip()
        elif line.startswith('A') and ':' in line and current_q:
            qa_list.append({"question": current_q, "answer": line.split(':', 1)[1].strip()})
            current_q = None
    return qa_list


def export_pdf(qa_list, role, level, round_type):
    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.add_page()
    pw = pdf.w - 2 * pdf.l_margin
    pdf.set_fill_color(14, 17, 23)
    pdf.set_text_color(232, 237, 245)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(pw, 14, "Interview Simulator Report", ln=True, align="C", fill=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(107, 122, 153)
    pdf.ln(3)
    pdf.cell(pw, 6, f"{role}  /  {level}  /  {round_type}", ln=True, align="C")
    pdf.ln(10)
    for i, qa in enumerate(qa_list, 1):
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(91, 156, 246)
        pdf.cell(pw, 5, f"QUESTION {i:02d}", ln=True)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(232, 237, 245)
        pdf.multi_cell(pw, 7, qa['question'])
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(107, 122, 153)
        pdf.multi_cell(pw, 6, qa['answer'])
        pdf.ln(6)
    path = os.path.join(tempfile.gettempdir(), "interview_report.pdf")
    pdf.output(path)
    return path


# ══════════════════════════════════
# LEFT PANEL (fixed via CSS)
# ══════════════════════════════════
left_col, right_col = st.columns([1, 1.7], gap="large")

with left_col:
    st.markdown("""
    <div class="logo-row">
        <div class="logo-pill">
            <div class="logo-dot"></div>
            <span class="logo-label">Interview Simulator</span>
        </div>
    </div>
    <div class="section-label">// Configuration</div>
    """, unsafe_allow_html=True)

    role = st.selectbox("Role", [
        "AI / ML Engineer", "Data Scientist", "Frontend Developer",
        "Backend Developer", "DevOps Engineer", "Cloud Engineer", "Full Stack Developer",
    ])
    level = st.selectbox("Experience Level", [
        "Fresher (0 years)", "Junior (1-2 years)", "Mid-level (2-4 years)",
        "Senior (4-6 years)", "5+ years"
    ])
    round_type = st.selectbox("Interview Round", [
        "Technical Round 1", "Technical Round 2", "System Design Round", "HR Round"
    ])
    topics = st.multiselect("Topics", [
        "Python", "Machine Learning", "Deep Learning", "LLMs", "RAG",
        "MLOps", "React", "Node.js", "SQL", "AWS", "Docker", "Kubernetes",
        "System Design", "Data Structures & Algorithms"
    ], default=["Python", "Machine Learning"])
    num_questions = st.slider("Number of Questions", 3, 15, 5)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Interview", use_container_width=True)


# ══════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════
with right_col:
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">AI-Powered Tool</div>
        <div class="hero-title">Interview Simulator</div>
        <div class="hero-desc">Generate structured, role-specific technical interview questions — tailored to your experience level and focus areas.</div>
        <div class="hero-line"></div>
    </div>
    """, unsafe_allow_html=True)

    if "qa_list" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">◈</div>
            <div class="empty-text">
                Configure your settings on the left<br/>
                then press Generate Interview<br/>
                to begin your session
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        qa_list = st.session_state["qa_list"]
        meta = st.session_state["meta"]
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in meta["topics"]])

        st.markdown(f"""
        <div class="results-meta">
            <div class="meta-role">{meta['role']} — {meta['round_type']}</div>
            <div class="meta-sub">{meta['level']} · {len(qa_list)} questions generated</div>
            <div>{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

        for i, qa in enumerate(qa_list, 1):
            st.markdown(f"""
            <div class="q-card">
                <span class="q-badge">Q {i:02d}</span>
                <div class="q-text">{qa['question']}</div>
                <div class="a-row">
                    <span class="a-badge">ans</span>
                    <div class="a-text">{qa['answer']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="export-row"></div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 4rem"></div>', unsafe_allow_html=True)
        col_exp, _ = st.columns([1, 2])
        with col_exp:
            if st.button("Export as PDF", use_container_width=True):
                pdf_path = export_pdf(qa_list, meta["role"], meta["level"], meta["round_type"])
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download PDF Report", data=f,
                        file_name="interview_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

# ── Generate Logic ──
if generate_btn:
    if not API_KEY:
        with left_col:
            st.error("API Key not found.")
    elif not topics:
        with left_col:
            st.error("Please select at least one topic.")
    else:
        with right_col:
            with st.spinner("Generating questions..."):
                try:
                    raw = generate_questions(role, topics, level, round_type, num_questions)
                    qa_list = parse_qa(raw)
                    if not qa_list:
                        st.error("Parsing failed. Try again.")
                    else:
                        st.session_state["qa_list"] = qa_list
                        st.session_state["meta"] = {
                            "role": role, "level": level,
                            "round_type": round_type, "topics": topics
                        }
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")