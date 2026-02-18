import streamlit as st
from google import genai

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Studio",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #7ee8a2;
    --accent2:   #38bdf8;
    --muted:     #4a4a6a;
    --text:      #e2e2f0;
    --text-dim:  #8888aa;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer { visibility: hidden; }

/* ── Main container ── */
.main .block-container {
    max-width: 760px !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    line-height: 1.05 !important;
    color: var(--text) !important;
    margin: 0 0 0.5rem !important;
    letter-spacing: -0.03em !important;
}
.hero h1 span { color: var(--accent); }
.hero p {
    color: var(--text-dim);
    font-size: 0.85rem;
    margin: 0;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Section label ── */
.section-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(126,232,162,0.08) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    color: var(--text-dim) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Slider ── */
[data-testid="stSlider"] .stSlider > div > div > div {
    background: var(--accent) !important;
}

/* ── Button ── */
[data-testid="stButton"] button {
    width: 100%;
    background: var(--accent) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 1.5rem !important;
    transition: opacity 0.15s ease, transform 0.15s ease !important;
    cursor: pointer !important;
}
[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Response card ── */
.response-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    margin-top: 1.5rem;
    font-size: 0.84rem;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}
.response-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.response-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse 1.5s ease infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
.response-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
}

/* ── Stats row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.stat-chip {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 0.25rem 0.75rem;
    border-radius: 100px;
}

/* ── Warning / Error ── */
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-dim) !important;
    font-size: 0.78rem !important;
}

/* ── Expander (settings) ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-dim) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Google DeepMind</div>
    <h1>Gemini <span>Studio</span></h1>
    <p>gemini-2.5-flash · conversational intelligence</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of (prompt, response) tuples

# ── Settings panel ───────────────────────────────────────────────────────────
with st.expander("⚙  Configuration"):
    api_key = st.text_input(
        "Google API Key",
        type="password",
        placeholder="AIza...",
        help="Get your key from https://aistudio.google.com/app/apikey",
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0, max_value=2.0, value=1.0, step=0.05,
        help="Higher = more creative, lower = more focused",
    )

st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

# ── Prompt input ─────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Your Prompt</p>', unsafe_allow_html=True)
prompt = st.text_area(
    label="prompt",
    label_visibility="collapsed",
    placeholder="Ask me anything — explain quantum entanglement, write a poem, debug my code…",
    height=140,
)

generate_clicked = st.button("✦  Generate Response")

# ── Generation logic ──────────────────────────────────────────────────────────
if generate_clicked:
    if not api_key:
        st.warning("Please enter your Google API Key in the Configuration panel above.")
    elif not prompt.strip():
        st.warning("Please enter a prompt before generating.")
    else:
        with st.spinner("Thinking…"):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"temperature": temperature},
                )
                result_text = response.text
                st.session_state.history.append((prompt.strip(), result_text))
            except Exception as e:
                st.error(f"Error: {e}")
                result_text = None

# ── Display latest response ───────────────────────────────────────────────────
if st.session_state.history:
    last_prompt, last_response = st.session_state.history[-1]
    word_count = len(last_response.split())
    char_count = len(last_response)

    st.markdown(f"""
    <div class="response-card">
        <div class="response-header">
            <div class="response-dot"></div>
            <span class="response-title">Gemini Response</span>
        </div>
        {last_response.replace('<', '&lt;').replace('>', '&gt;')}
    </div>
    <div class="stats-row">
        <span class="stat-chip">✦ {word_count} words</span>
        <span class="stat-chip">✦ {char_count} chars</span>
        <span class="stat-chip">✦ temp {temperature:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    # Copy-friendly expander
    with st.expander("📋  Raw text (copy-friendly)"):
        st.code(last_response, language=None)

# ── History ───────────────────────────────────────────────────────────────────
if len(st.session_state.history) > 1:
    st.markdown('<div class="divider" style="margin:2rem 0 1.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Previous Prompts</p>', unsafe_allow_html=True)
    for i, (p, r) in enumerate(reversed(st.session_state.history[:-1]), 1):
        with st.expander(f"#{len(st.session_state.history)-i}  {p[:60]}{'…' if len(p)>60 else ''}"):
            st.markdown(f"""
            <div style="font-size:0.8rem;color:#8888aa;line-height:1.8;white-space:pre-wrap">
            {r.replace('<','&lt;').replace('>','&gt;')}
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;color:#2e2e4e;font-size:0.62rem;letter-spacing:0.15em;text-transform:uppercase">
    Gemini Studio · Built with Streamlit
</div>
""", unsafe_allow_html=True)