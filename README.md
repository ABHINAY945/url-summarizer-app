# 🦜 SummarizeAI — Instant YT & Web Summaries

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3-orange)

A beautifully designed, premium Streamlit web application that instantly generates concise summaries of YouTube videos and website articles. Powered by **LangChain** and **Groq's Llama 3.3** model for blazing-fast inference.

## ✨ Features

- **🎬 YouTube Video Summarization**: Automatically extracts transcripts from YouTube links and summarizes the video content.
- **🌐 Web Article Summarization**: Scrapes and synthesizes content from any standard website or blog post.
- **⚡ Powered by Llama 3.3**: Utilizes the ultra-fast Groq API running the `llama-3.3-70b-versatile` model.
- **💎 Premium UI**: Features a modern dark theme, custom Google Fonts (Outfit & Inter), and interactive glassmorphism UI components.
- **🔒 Secure & Local**: Bring your own API key. Keys are used at runtime and not stored anywhere.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) with custom CSS
- **Orchestration**: [LangChain](https://python.langchain.com/)
- **LLM Provider**: [Groq API](https://console.groq.com/)
- **Document Loaders**: `YoutubeLoader`, `UnstructuredURLLoader`

## 🚀 Getting Started

Follow these steps to set up the project locally on your machine.

### Prerequisites

- Python 3.9 or higher
- A free [Groq API Key](https://console.groq.com/keys)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/url-summarizer-app.git
   cd url-summarizer-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💡 How to Use

1. Launch the app and open it in your browser (usually `http://localhost:8501`).
2. In the sidebar, paste your **Groq API Key**.
3. Paste a valid **YouTube URL** or **Website URL** in the main input field.
4. Click **✨ Summarize Content**.
5. Wait a few seconds for the AI to analyze the content and generate a concise 300-word summary!


### 🌐 Live Demo
👉 https://url-summarizer-app-r3mgh7jrewr8rdurssuzjh.streamlit.app/



