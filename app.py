import os
import validators, streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_groq import ChatGroq
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# Load environment variables
load_dotenv()

# ──────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SummarizeAI — Instant YT & Web Summaries",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# Custom CSS — Premium dark theme with Outfit + Inter fonts
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Root variables ── */
    :root {
        --bg-primary:    #0a0a0f;
        --bg-card:       rgba(255, 255, 255, 0.04);
        --bg-card-hover: rgba(255, 255, 255, 0.07);
        --border-glass:  rgba(255, 255, 255, 0.08);
        --text-primary:  #e8e8f0;
        --text-muted:    #8b8ba3;
        --accent-start:  #6c5ce7;
        --accent-end:    #a29bfe;
        --accent-glow:   rgba(108, 92, 231, 0.35);
        --success-start: #00b894;
        --success-end:   #55efc4;
        --danger:        #ff6b6b;
        --radius:        16px;
        --transition:    0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Global resets ── */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Remove Streamlit header / footer ── */
    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d15 0%, #111122 100%) !important;
        border-right: 1px solid var(--border-glass) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }
    [data-testid="stSidebar"] label {
        font-weight: 500;
        letter-spacing: 0.02em;
        color: var(--text-muted) !important;
        text-transform: uppercase;
        font-size: 0.7rem !important;
    }

    /* ── Headings ── */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* ── Text inputs ── */
    [data-testid="stTextInput"] input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-glass) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: var(--transition) !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--accent-start) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: var(--text-muted) !important;
        opacity: 0.6;
    }

    /* ── Primary button ── */
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, var(--accent-start), var(--accent-end)) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.01em;
        padding: 0.7rem 2rem !important;
        cursor: pointer;
        transition: var(--transition) !important;
        box-shadow: 0 4px 20px var(--accent-glow) !important;
    }
    [data-testid="stButton"] > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 30px var(--accent-glow) !important;
        filter: brightness(1.1);
    }
    [data-testid="stButton"] > button:active {
        transform: translateY(0) scale(0.98);
    }

    /* ── Success alert (summary output) ── */
    [data-testid="stAlert"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-glass) !important;
        border-left: 4px solid var(--success-start) !important;
        border-radius: var(--radius) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 1.5rem !important;
        animation: fadeSlideUp 0.5s ease-out;
    }
    [data-testid="stAlert"] p {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
        line-height: 1.7 !important;
        font-size: 0.95rem !important;
    }

    /* ── Error messages ── */
    .stException, div[data-testid="stException"] {
        border-radius: var(--radius) !important;
    }

    /* ── Spinner ── */
    [data-testid="stSpinner"] {
        color: var(--accent-end) !important;
    }
    [data-testid="stSpinner"] > div > span {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-muted) !important;
    }

    /* ── Divider ── */
    hr {
        border-color: var(--border-glass) !important;
        margin: 2rem 0 !important;
    }

    /* ── Animations ── */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 20px var(--accent-glow); }
        50%      { box-shadow: 0 0 40px var(--accent-glow); }
    }

    /* ── Animated hero gradient text ── */
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        background: linear-gradient(135deg, #6c5ce7, #a29bfe, #74b9ff, #6c5ce7);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 6s ease infinite;
        margin-bottom: 0.3rem;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.05rem;
        color: var(--text-muted);
        margin-bottom: 1.8rem;
        letter-spacing: 0.01em;
    }



    /* ── Feature pills ── */
    .feature-row {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }
    .feature-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: 99px;
        padding: 0.4rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--text-muted);
        letter-spacing: 0.02em;
        transition: var(--transition);
    }
    .feature-pill:hover {
        background: var(--bg-card-hover);
        color: var(--text-primary);
        border-color: var(--accent-start);
    }

    /* ── Footer badge ── */
    .footer-badge {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        letter-spacing: 0.04em;
    }
    .footer-badge a {
        color: var(--accent-end);
        text-decoration: none;
        font-weight: 500;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb {
        background: rgba(108, 92, 231, 0.3);
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(108, 92, 231, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# Sidebar — API key
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### 🔑 Configuration")
    groq_api_key = st.text_input(
        "Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        help="Get your free API key from https://console.groq.com",
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.78rem; color:#8b8ba3; line-height:1.6;">
        <b style="color:#a29bfe;">How it works</b><br>
        1. Paste your Groq API key<br>
        2. Enter a YouTube or website URL<br>
        3. Click <b>Summarize</b> and get instant results
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────
# Hero section
# ──────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">Summarize Any URL ✨</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Paste a YouTube video or website link and get a concise AI-powered summary in seconds.</p>',
    unsafe_allow_html=True,
)

# Feature pills
st.markdown(
    """
    <div class="feature-row">
        <span class="feature-pill">🎬 YouTube Videos</span>
        <span class="feature-pill">🌐 Web Articles</span>
        <span class="feature-pill">⚡ Powered by Llama 3.3</span>
        <span class="feature-pill">🔒 Secure</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# URL input
# ──────────────────────────────────────────────────────────────
st.markdown(
    "<span style='font-family:Outfit,sans-serif;font-weight:600;font-size:1.05rem;'>🔗 Enter the URL to summarize</span>",
    unsafe_allow_html=True,
)
generic_url = st.text_input("URL", label_visibility="collapsed", placeholder="https://youtube.com/watch?v=... or any website")

# ──────────────────────────────────────────────────────────────
# LLM setup
# ──────────────────────────────────────────────────────────────
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}

"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# ──────────────────────────────────────────────────────────────
# Summarize button & logic
# ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    summarize_clicked = st.button("✨  Summarize Content", use_container_width=True)

if summarize_clicked:
    # Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("⚠️  Please provide both a Groq API key and a URL to get started.")
    elif not validators.url(generic_url):
        st.error("🚫  Please enter a valid URL — it can be a YouTube video or any website link.")
    else:
        try:
            with st.spinner("🧠 Analyzing content — hang tight…"):
                # Load content
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=False)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/116.0.0.0 Safari/537.36"
                        },
                    )
                docs = loader.load()

                # Summarize
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

            # Display result
            st.markdown("---")
            st.markdown(
                "<span style='font-family:Outfit,sans-serif;font-weight:700;font-size:1.2rem;'>"
                "📋 Summary</span>",
                unsafe_allow_html=True,
            )
            st.success(output_summary)

        except Exception as e:
            st.exception(e)

# ──────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-badge">Built with 🦜 LangChain · Groq · Streamlit</div>',
    unsafe_allow_html=True,
)