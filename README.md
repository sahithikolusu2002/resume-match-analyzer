# Resume Analyzer

A FastAPI-based application that extracts resume content and analyzes it against a job description using Ollama.

## Features
- PDF/DOCX resume text extraction
- LLM-based skill matching and recommendations
- STAR-based interview prep
- Project highlights and learning path suggestions

**🧠 Step-by-Step Guide: Running Resume Analyzer with Ollama + FastAPI + Gradio**<br>
✅ 1. **Install Ollama**<br>
Ollama lets you run large language models (LLMs) like OpenChat locally.<br>
Install Ollama: **https://ollama.com/download**<br>
Download and install for your OS (macOS, Windows, or Linux).
After installing, make sure ollama is accessible via terminal:
**ollama --version**

✅ 2. **Pull the OpenChat model**<br>
Run the following in your terminal:
**ollama run openchat**<br>
This will:
Download the OpenChat model<br>
Start an interactive shell (you can Ctrl+C to exit after confirming it works)

✅ 3. R**un your FastAPI backend**<br>
Navigate to your project’s backend/ directory (where main.py is):<br>

**cd project-folder<br>
uvicorn main:app --reload**<br>
This starts the FastAPI server at:
**📍 http://127.0.0.1:8000**<br>
Make sure Ollama is still running and listening at http://localhost:11434.

✅ 4. **Run the Gradio Frontend UI**<br>
In another terminal (still in the backend/ folder), run:
**python ui.py**<br>
This will launch the Gradio interface locally. You’ll get a link like:<br>
Running on local URL:  **http://127.0.0.1:7860/**

**🧪 Testing Flow**<br>
ollama run openchat — load the LLM<br>
uvicorn main:app --reload — start API server<br>
python ui.py — start Gradio UI<br>
Open the Gradio link → upload your resume + paste job description → receive analy<br>
