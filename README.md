# Resume Intelligence Engine

A modern, editorial-style workspace powered by Groq AI and Streamlit to evaluate resumes, analyze job requirements, identify improvement opportunities, and build polished professional CVs.

---

## Features

- Dual Analysis Modes:
  - With Job Requirements: Compares your CV against a specific job description and calculates a targeted job-match score.
  - Without Job Requirements: Independently evaluates overall CV quality, formatting, ATS compatibility, and core skills.
- AI Resume Builder: Dynamically generates optimized resume sections using Groq AI.
- PDF Intelligence Pipeline: Extract data smoothly from uploaded files and export generated reports into clean, printable PDFs.
- Tailored Aesthetic Layout: Custom web UI built using an elegant, warm editorial layout with refined typography and soft ivory tones.

---

## Architecture and Tech Stack

- Framework: Streamlit
- LLM Core: Groq API Cloud
- PDF Extraction: PyMuPDF (fitz)
- Document Engine: ReportLab

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com
cd resume-intelligence-engine
```

### 2. Install Dependencies
Install the required packages using pip:
```bash
pip install streamlit groq pymupdf reportlab
```

### 3. Set Up Your API Credentials
You have to add your own Groq API key configuration before launching the application. Replace the placeholder with your actual Groq cloud console API link credentials.

On Windows (PowerShell):
```powershell
\$env:GROQ_API_KEY = "your_groq_api_key_here"
```

On Linux / macOS:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 4. Launch the Web Application
Run the main script file via Streamlit:
```bash
streamlit run Step3_analyze.py
```

---

## UI and Styling Architecture

The application bypasses the default industrial dashboard look in favor of an editorial magazine aesthetic:
- Typography: Refined font hierarchy balancing Playfair Display serif headers with highly readable DM Sans body text.
- Color Palette: Warm ivory background backgrounds (#F6F4EF), clean card surfaces (#FFFFFF), with earthy terracotta and muted sage accents.
