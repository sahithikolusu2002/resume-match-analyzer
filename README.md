# Resume Analyzer

A FastAPI-based application that extracts resume content and analyzes it against a job description using Ollama.

## Features
- PDF/DOCX resume text extraction
- LLM-based skill matching and recommendations
- STAR-based interview prep
- Project highlights and learning path suggestions

**🧠 Step-by-Step Guide: Running Resume Analyzer with Ollama + FastAPI + Gradio**
✅ 1. Install Ollama
Ollama lets you run large language models (LLMs) like OpenChat locally.

Install Ollama:
Visit: **https://ollama.com/download**
Download and install for your OS (macOS, Windows, or Linux).

After installing, make sure ollama is accessible via terminal:
**ollama --version**

✅ 2. Pull the OpenChat model
Run the following in your terminal:
**ollama run openchat**
This will:
Download the OpenChat model
Start an interactive shell (you can Ctrl+C to exit after confirming it works)

✅ 3. Run your FastAPI backend
Navigate to your project’s backend/ directory (where main.py is):

**cd project-folder
uvicorn main:app --reload**
This starts the FastAPI server at:
**📍 http://127.0.0.1:8000**
Make sure Ollama is still running and listening at http://localhost:11434.

✅ 4. Run the Gradio Frontend UI
In another terminal (still in the backend/ folder), run:
**python ui.py**
This will launch the Gradio interface locally. You’ll get a link like:
Running on local URL:  **http://127.0.0.1:7860/**

**🧪 Testing Flow**
ollama run openchat — load the LLM
uvicorn main:app --reload — start API server
python ui.py — start Gradio UI
Open the Gradio link → upload your resume + paste job description → receive analy
