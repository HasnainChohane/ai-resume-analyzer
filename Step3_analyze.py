
import io
import os
import re
import html
import fitz
import streamlit as st

from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib import colors


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Resume Intelligence Engine",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_KEY ="add yours"
MODEL = "openai/gpt-oss-20b"

client = Groq(api_key=API_KEY) if API_KEY else None


# =========================================================
# CUSTOM THEME
# =========================================================

def load_styles():

    st.markdown("""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap'
    );

    :root {
        --background: #F6F4EF;
        --surface: #FFFFFF;
        --text: #292D29;
        --muted: #777D73;
        --border: #E8E5DC;
        --sage: #718575;
        --sage-light: #EDF1EB;
        --terracotta: #BD765C;
        --terracotta-light: #F7EDE8;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1160px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4 {
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
    }

    p, li, label {
        color: #50564F;
    }

    /* Main hero */

    .hero {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 38px;
        margin-bottom: 25px;
        box-shadow: 0 4px 18px rgba(45, 48, 38, 0.035);
    }

    .brand {
        color: var(--terracotta);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 2.5px;
        margin-bottom: 15px;
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        color: #292D29;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #777D73;
        font-size: 1rem;
        line-height: 1.8;
        max-width: 760px;
    }

    .section-title {
        color: #292D29;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .section-description {
        color: #777D73;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Cards */

    .custom-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(45, 48, 38, 0.025);
    }

    .result-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 23px;
        margin-bottom: 17px;
    }

    .score-card {
        background: var(--sage-light);
        border: 1px solid #DCE5D9;
        border-left: 5px solid var(--sage);
        border-radius: 12px;
        padding: 22px;
        margin: 16px 0;
    }

    .score-label {
        color: #657366;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .score-value {
        color: #394D3D;
        font-size: 2.7rem;
        font-weight: 800;
        margin-top: 5px;
    }

    /* Buttons */

    .stButton > button {
        background: var(--sage);
        color: #FFFFFF !important;
        border: 1px solid var(--sage);
        border-radius: 9px;
        min-height: 44px;
        font-weight: 700;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #5D7161;
        border-color: #5D7161;
        color: #FFFFFF !important;
    }

    .stDownloadButton > button {
        background: #FFFFFF;
        color: #526B58 !important;
        border: 1px solid #A9B9A9;
        border-radius: 9px;
        min-height: 43px;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        background: var(--sage-light);
        border-color: var(--sage);
    }

    /* Input fields */

    .stTextInput input,
    .stTextArea textarea {
        background: #FFFFFF !important;
        color: #292D29 !important;
        border: 1px solid #DDDCD3 !important;
        border-radius: 9px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--sage) !important;
        box-shadow: 0 0 0 2px rgba(113, 133, 117, 0.12);
    }

    [data-testid="stFileUploader"] {
        background: #FFFFFF;
        border: 1px dashed #C9C9BB;
        border-radius: 12px;
        padding: 15px;
    }

    [data-testid="stFileUploader"] section {
        background: #FFFFFF;
    }

    /* Metrics */

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        color: #777D73 !important;
    }

    [data-testid="stMetricValue"] {
        color: #292D29 !important;
    }

    /* Radio buttons */

    [data-testid="stRadio"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 15px;
    }

    /* Expanders and alerts */

    [data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: var(--border);
    }

    /* Footer */

    .footer {
        text-align: center;
        color: #96988F;
        font-size: 0.8rem;
        line-height: 1.8;
        margin-top: 45px;
        padding-top: 22px;
        border-top: 1px solid var(--border);
    }

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 23px;
        }

        .hero-title {
            font-size: 1.9rem;
        }

        .custom-card,
        .result-card {
            padding: 17px;
        }

    }

    </style>
    """, unsafe_allow_html=True)


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_text_from_pdf(pdf_file):

    pdf_file.seek(0)

    document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    pages = [
        page.get_text()
        for page in document
    ]

    document.close()

    return "\n".join(pages).strip()


# =========================================================
# AI RESUME ANALYSIS
# =========================================================

def analyze_resume_comprehensive(
    resume_text,
    job_requirements=None
):

    if job_requirements:

        analysis_instruction = f"""
Analyze the candidate's resume against the specific
job requirements below.

Calculate a JOB MATCH SCORE from 0 to 100.

Evaluate:
- Required skills and technologies
- Relevant work experience
- Education and qualifications
- Project relevance
- Missing requirements
- Overall suitability for the position

Do not invent candidate qualifications.

JOB REQUIREMENTS:
{job_requirements}

Use this exact output structure:

SCORE: [number from 0 to 100]

ANALYSIS TYPE:
Job-Specific Resume Analysis

TARGET REQUIREMENTS:
List the important requirements for the position.

MATCHING SKILLS:
List the skills and qualifications the candidate already has.

MISSING SKILLS:
List important requirements not demonstrated in the resume.

SUITABLE JOB ROLES:
Suggest three relevant job titles.

EVALUATION SUMMARY:

1. Overall Impression
2. Strengths
3. Weaknesses
4. Top 3 Improvement Suggestions
5. Final Recommendation
"""

    else:

        analysis_instruction = """
Analyze the resume independently without comparing it
against a particular job description.

Calculate an OVERALL RESUME QUALITY SCORE from 0 to 100.

Evaluate:
- Resume structure and organization
- Professional presentation
- ATS readability and compatibility
- Education and experience presentation
- Technical and professional skills
- Projects and achievements
- Grammar and clarity
- Completeness and consistency

Do not assume a specific target job.
Do not penalize the candidate for not providing
a job description.
Do not invent candidate qualifications.

Use this exact output structure:

SCORE: [number from 0 to 100]

ANALYSIS TYPE:
General Resume Quality Analysis

RESUME QUALITY CRITERIA:
Evaluate the structure, readability, ATS compatibility,
content quality, skills, and completeness.

KEY STRENGTHS:
List the strongest aspects of this resume.

AREAS FOR IMPROVEMENT:
Identify missing information, weak descriptions,
formatting issues, and other problems.

SUITABLE JOB ROLES:
Suggest three realistic job titles based on the
candidate's actual qualifications.

EVALUATION SUMMARY:

1. Overall Impression
2. Professional Presentation
3. ATS Compatibility
4. Content and Experience Quality
5. Top 5 Improvement Suggestions
6. Final Recommendation
"""

    prompt = f"""
You are a senior recruitment consultant,
professional resume auditor, and ATS specialist.

Your task is to provide an honest, detailed,
constructive resume evaluation.

{analysis_instruction}

IMPORTANT:
- Give a score based on actual resume evidence.
- Never invent qualifications or experience.
- Be specific and practical.
- Use clear headings and readable bullet points.
- Distinguish missing information from missing skills.

CANDIDATE RESUME:
{resume_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert resume reviewer "
                    "and professional recruitment consultant."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# =========================================================
# AI RESUME BUILDER
# =========================================================

def build_resume_from_inputs(user_data):

    prompt = f"""
You are an expert professional resume writer.

Create a polished, ATS-friendly professional resume
using the information provided below.

INSTRUCTIONS:

- Use professional language.
- Organize information into clear sections.
- Improve grammar and sentence structure.
- Use strong action verbs where appropriate.
- Keep the resume readable and concise.
- Do not invent qualifications or experience.
- Do not add information that was not provided.
- Use a professional resume structure.
- Prioritize relevant achievements and skills.

CANDIDATE INFORMATION:

{user_data}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert technical resume writer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


# =========================================================
# ANALYSIS RESULT PARSER
# =========================================================

def parse_analysis(raw_output):

    sections = {
        "score": "N/A",
        "targets": "",
        "strengths": "",
        "missing": "",
        "roles": "",
        "evaluation": raw_output
    }

    score_match = re.search(
        r"SCORE:\s*(\d{1,3})",
        raw_output,
        re.IGNORECASE
    )

    if score_match:

        score = int(score_match.group(1))

        if 0 <= score <= 100:
            sections["score"] = score

    def extract_section(start, end_options):

        pattern = (
            re.escape(start)
            + r"\s*(.*?)"
            + r"(?="
            + "|".join(
                re.escape(item)
                for item in end_options
            )
            + r"|$)"
        )

        match = re.search(
            pattern,
            raw_output,
            re.IGNORECASE | re.DOTALL
        )

        return match.group(1).strip() if match else ""

    sections["targets"] = extract_section(
        "TARGET REQUIREMENTS",
        [
            "MATCHING SKILLS",
            "RESUME QUALITY CRITERIA",
            "KEY STRENGTHS",
            "SUITABLE JOB ROLES"
        ]
    )

    sections["strengths"] = extract_section(
        "MATCHING SKILLS",
        [
            "MISSING SKILLS",
            "SUITABLE JOB ROLES"
        ]
    )

    sections["missing"] = extract_section(
        "MISSING SKILLS",
        [
            "SUITABLE JOB ROLES",
            "EVALUATION SUMMARY"
        ]
    )

    if not sections["missing"]:
        sections["missing"] = extract_section(
            "AREAS FOR IMPROVEMENT",
            [
                "SUITABLE JOB ROLES",
                "EVALUATION SUMMARY"
            ]
        )

    sections["roles"] = extract_section(
        "SUITABLE JOB ROLES",
        ["EVALUATION SUMMARY"]
    )

    evaluation_match = re.search(
        r"EVALUATION SUMMARY:\s*(.*)",
        raw_output,
        re.IGNORECASE | re.DOTALL
    )

    if evaluation_match:
        sections["evaluation"] = (
            evaluation_match.group(1).strip()
        )

    return sections


# =========================================================
# PDF GENERATOR
# =========================================================

def generate_minimal_pdf(document_text):

    buffer = io.BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocumentTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#303B32"),
        spaceAfter=16
    )

    heading_style = ParagraphStyle(
        "DocumentHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#718575"),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "DocumentBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#30342F"),
        spaceAfter=5
    )

    story = []

    for index, line in enumerate(document_text.split("\n")):

        clean_line = line.strip()

        if not clean_line:
            story.append(Spacer(1, 4))
            continue

        safe_line = html.escape(clean_line)

        if index == 0:

            story.append(
                Paragraph(safe_line, title_style)
            )

        elif (
            clean_line.isupper()
            and len(clean_line) < 65
        ):

            story.append(
                Paragraph(safe_line, heading_style)
            )

        else:

            story.append(
                Paragraph(safe_line, body_style)
            )

    pdf.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# RESUME ANALYSIS PAGE
# =========================================================

def analysis_page():

    st.markdown(
        '<div class="section-title">Resume Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Choose how you want your resume evaluated.'
        '</div>',
        unsafe_allow_html=True
    )

    analysis_mode = st.radio(
        "Analysis method",
        [
            "With Job Requirements",
            "Without Job Requirements"
        ],
        horizontal=True,
        key="analysis_mode"
    )

    job_requirements = ""

    if analysis_mode == "With Job Requirements":

        st.markdown(
            '<div class="custom-card">',
            unsafe_allow_html=True
        )

        st.subheader("Target Job Description")

        job_requirements = st.text_area(
            "Enter job description and requirements",
            height=160,
            placeholder=(
                "Paste the job description, required skills, "
                "responsibilities, and qualifications..."
            )
        )

        st.caption(
            "Your resume will be evaluated against this "
            "specific job description."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.markdown(
            '<div class="custom-card">',
            unsafe_allow_html=True
        )

        st.subheader("General Resume Evaluation")

        st.write(
            "No job description is needed. The AI will "
            "evaluate your CV independently, including "
            "its structure, ATS readability, skills, "
            "experience, and professional presentation."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"],
        key="analysis_pdf"
    )

    if st.button(
        "Analyze My CV",
        use_container_width=True
    ):

        if uploaded_file is None:

            st.warning("Please upload your CV first.")

        elif (
            analysis_mode == "With Job Requirements"
            and not job_requirements.strip()
        ):

            st.warning(
                "Please enter the job requirements "
                "or select the general analysis option."
            )

        else:

            try:

                with st.spinner(
                    "Analyzing your CV with AI..."
                ):

                    resume_text = extract_text_from_pdf(
                        uploaded_file
                    )

                    if not resume_text:

                        st.error(
                            "No readable text was found. "
                            "Your PDF may contain scanned images."
                        )
                        st.stop()

                    raw_output = analyze_resume_comprehensive(
                        resume_text,
                        job_requirements
                        if analysis_mode == "With Job Requirements"
                        else None
                    )

                    st.session_state.analysis_result = (
                        parse_analysis(raw_output)
                    )

                    st.session_state.analysis_type = (
                        analysis_mode
                    )

            except Exception as error:

                st.error(
                    f"Analysis failed: {error}"
                )

    # Display analysis

    if "analysis_result" in st.session_state:

        result = st.session_state.analysis_result

        st.markdown(
            '<div class="section-title">Analysis Results</div>',
            unsafe_allow_html=True
        )

        st.caption(
            f"Analysis type: {st.session_state.analysis_type}"
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            st.markdown(
                '<div class="score-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="score-label">RESUME SCORE</div>',
                unsafe_allow_html=True
            )

            score_text = (
                f"{result['score']}%"
                if result["score"] != "N/A"
                else "N/A"
            )

            st.markdown(
                f'<div class="score-value">{score_text}</div>',
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown("**AI Model**")

            st.write(MODEL)

            st.markdown("**Evaluation Type**")

            st.write(st.session_state.analysis_type)

            st.markdown("</div>", unsafe_allow_html=True)

        if result["targets"]:

            with st.expander(
                "Requirements / Resume Quality Criteria",
                expanded=True
            ):

                st.markdown(result["targets"])

        if result["strengths"]:

            with st.expander(
                "Matching Skills / Key Strengths",
                expanded=True
            ):

                st.markdown(result["strengths"])

        if result["missing"]:

            with st.expander(
                "Missing Skills / Areas for Improvement",
                expanded=True
            ):

                st.markdown(result["missing"])

        if result["roles"]:

            with st.expander(
                "Suitable Job Roles",
                expanded=True
            ):

                st.markdown(result["roles"])

        st.markdown(
            '<div class="section-title">'
            'Detailed Evaluation'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown(result["evaluation"])

        st.markdown("</div>", unsafe_allow_html=True)

        report = f"""
RESUME INTELLIGENCE ENGINE
RESUME ANALYSIS REPORT

ANALYSIS TYPE:
{st.session_state.analysis_type}

RESUME SCORE:
{result['score']}%

REQUIREMENTS / QUALITY CRITERIA:
{result['targets']}

MATCHING SKILLS / KEY STRENGTHS:
{result['strengths']}

MISSING SKILLS / IMPROVEMENTS:
{result['missing']}

SUITABLE JOB ROLES:
{result['roles']}

DETAILED EVALUATION:
{result['evaluation']}
"""

        pdf_data = generate_minimal_pdf(report)

        st.download_button(
            "Download Analysis Report PDF",
            data=pdf_data,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
# AI RESUME BUILDER PAGE
# =========================================================

def builder_page():

    st.markdown(
        '<div class="section-title">'
        'AI Professional Resume Builder'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Provide your information and generate a '
        'professional, ATS-friendly resume.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("resume_builder_form"):

        st.subheader("Personal Information")

        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        contact_info = st.text_input(
            "Contact Information",
            placeholder="Email | Phone | City | LinkedIn"
        )

        st.divider()

        st.subheader("Education")

        education = st.text_area(
            "Education Details",
            height=100,
            placeholder=(
                "Degree, university, CGPA, graduation year..."
            )
        )

        st.divider()

        st.subheader("Professional Experience")

        experience = st.text_area(
            "Experience / Internships",
            height=140,
            placeholder=(
                "Company, job title, responsibilities, "
                "achievements, and duration..."
            )
        )

        st.divider()

        st.subheader("Technical Skills")

        skills_tools = st.text_area(
            "Skills and Technologies",
            height=100,
            placeholder=(
                "Programming languages, frameworks, "
                "databases, tools, and technologies..."
            )
        )

        st.divider()

        st.subheader("Projects and Certifications")

        projects = st.text_area(
            "Projects and Certifications",
            height=110,
            placeholder=(
                "Project names, descriptions, technologies, "
                "certificates, and achievements..."
            )
        )

        submitted = st.form_submit_button(
            "Generate Professional Resume",
            use_container_width=True
        )

    if submitted:

        if not full_name.strip():

            st.warning("Please enter your full name.")

        elif not experience.strip() and not projects.strip():

            st.warning(
                "Please provide experience or project details."
            )

        else:

            user_data = f"""
NAME:
{full_name}

CONTACT:
{contact_info}

EDUCATION:
{education}

EXPERIENCE:
{experience}

TECHNICAL SKILLS:
{skills_tools}

PROJECTS AND CERTIFICATIONS:
{projects}
"""

            try:

                with st.spinner(
                    "Generating your professional resume..."
                ):

                    generated_resume = build_resume_from_inputs(
                        user_data
                    )

                    st.session_state.generated_resume = (
                        generated_resume
                    )

            except Exception as error:

                st.error(
                    f"Resume generation failed: {error}"
                )

    if "generated_resume" in st.session_state:

        st.markdown(
            '<div class="section-title">'
            'Generated Resume Preview'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.generated_resume
        )

        st.markdown("</div>", unsafe_allow_html=True)

        resume_pdf = generate_minimal_pdf(
            st.session_state.generated_resume
        )

        st.download_button(
            "Download Professional Resume PDF",
            data=resume_pdf,
            file_name="professional_resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =========================================================
# MAIN APPLICATION
# =========================================================

def main():

    load_styles()

    if not API_KEY or not client:

        st.error(
            "Groq API key is missing. Please configure "
            "the GROQ_API_KEY environment variable."
        )

        st.stop()

    st.html("""
<div class="hero">
    <div class="brand">HASNAIN CHOHAN</div>
    <div class="hero-title">Resume Intelligence Engine</div>
    <div class="hero-description">
        A professional AI-powered workspace to evaluate resumes,
        identify improvement opportunities, and build polished professional CVs.
    </div>
</div>
""")


    page = st.radio(
        "Select Workspace",
        [
            "Resume Analysis",
            "AI Resume Builder"
        ],
        horizontal=True,
        key="main_page"
    )

    st.divider()

    if page == "Resume Analysis":

        analysis_page()

    else:

        builder_page()

    st.markdown("""
    <div class="footer">
        RESUME INTELLIGENCE ENGINE
        <br>
        Designed and Developed by Hasnain Chohan
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
