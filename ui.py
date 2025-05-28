# import gradio as gr
# import requests
# import json
# import io
# import os

# API_URL = "http://localhost:8000/analyze"

# def analyze_resume(resume_file, file_type_choice, interview_level, job_description):
#     if resume_file is None or job_description.strip() == "":
#         yield gr.update(value=""), gr.update(value="Please upload a resume and enter a job description.")
#         return

#     # Determine filename and content type based on user's choice and file extension
#     if isinstance(resume_file, str):
#         filename = resume_file
#     elif hasattr(resume_file, "name"):
#         filename = resume_file.name
#     else:
#         yield gr.update(value=""), gr.update(value="Invalid file input. Please try uploading the resume again.")
#         return

#     # Validate file type against user's choice
#     if file_type_choice == "PDF" and not filename.endswith(".pdf"):
#         yield gr.update(value=""), gr.update(value="Error: You selected PDF, but the uploaded file is not a PDF (.pdf).")
#         return
#     elif file_type_choice == "DOCX" and not filename.endswith(".docx"):
#         yield gr.update(value=""), gr.update(value="Error: You selected DOCX, but the uploaded file is not a DOCX (.docx).")
#         return

#     # Set content_type based on the file extension
#     if filename.endswith(".pdf"):
#         content_type = "application/pdf"
#     elif filename.endswith(".docx"):
#         content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     else:
#         yield gr.update(value=""), gr.update(value="Unsupported file type. Please upload a PDF or DOCX.")
#         return

#     # Read file bytes
#     try:
#         with open(filename, "rb") as f:
#             file_bytes = f.read()
#     except Exception as e:
#         yield gr.update(value=""), gr.update(value=f"Failed to read uploaded file: {e}")
#         return

#     file_stream = io.BytesIO(file_bytes)

#     files = {
#         "resume": (os.path.basename(filename), file_stream, content_type)
#     }
#     data = {
#         "job_description": job_description,
#         "interview_level": interview_level
#     }

#     try:
#         yield gr.update(value="🔄 Analyzing resume... Please wait..."), gr.update(value="")
        
#         response = requests.post(API_URL, files=files, data=data)
#         response.raise_for_status()
#         raw_output = response.json()

#         if "error" in raw_output:
#             yield gr.update(value=""), gr.update(value=f"**Backend Error:** {raw_output['error']}\n\nPlease check the FastAPI server logs.")
#             return
#         if "raw_response" in raw_output:
#             yield gr.update(value=""), gr.update(value=f"**Could not parse JSON from AI model. Raw response:**\n```json\n{raw_output['raw_response']}\n```\n\n")
#             return

#         matched_skills = raw_output.get("matched_skills", [])
#         missing_skills = raw_output.get("missing_skills", [])
        
#         # --- FIX FOR 'list' object has no attribute 'keys' ---
#         proficiency_levels_raw = raw_output.get("proficiency_levels", {})
#         proficiency_levels = {}
        
#         if isinstance(proficiency_levels_raw, dict):
#             proficiency_levels = proficiency_levels_raw
#         elif isinstance(proficiency_levels_raw, list):
#             # Attempt to parse a list of strings like ["Skill: Level", ...]
#             for item in proficiency_levels_raw:
#                 if isinstance(item, str) and ":" in item:
#                     try:
#                         skill, level = item.split(":", 1)
#                         proficiency_levels[skill.strip()] = level.strip()
#                     except ValueError:
#                         # Handle cases where parsing fails (e.g., "Skill Level" instead of "Skill: Level")
#                         pass 
#                 elif isinstance(item, dict) and "skill" in item and "level" in item:
#                     # Handle cases where it's a list of dicts like [{"skill": "Skill", "level": "Level"}]
#                     proficiency_levels[item["skill"].strip()] = item["level"].strip()
#         # --- END FIX ---

#         # --- Combined Table Logic ---
#         formatted_output = f"## 📝 Resume Analysis Results\n\n"
#         formatted_output += f"**Analysis Focus:** *{interview_level}*\n\n"

#         # Prepare data for the combined table
#         all_skills = sorted(list(set(matched_skills + missing_skills + list(proficiency_levels.keys()))))
        
#         if not all_skills:
#             formatted_output += "No relevant skills found for analysis.\n"
#         else:
#             formatted_output += "### 📊 Comprehensive Skill Analysis:\n"
#             formatted_output += "| Skill | Status | Proficiency Level |\n"
#             formatted_output += "|---|---|---|\n"

#             for skill in all_skills:
#                 status = ""
#                 if skill in matched_skills:
#                     status = "✅ Matched"
#                 elif skill in missing_skills:
#                     status = "⚠️ Missing"
#                 elif skill in proficiency_levels: 
#                     status = "➖ Mentioned" # If in prof levels but not matched/missing
#                 else: 
#                     status = "❓ Unknown"
                
#                 proficiency = proficiency_levels.get(skill, "N/A")
#                 formatted_output += f"| {skill} | {status} | {proficiency} |\n"
#             formatted_output += "\n"
#         # --- End Combined Table Logic ---

#         yield gr.update(value="Analysis Complete!"), gr.update(value=formatted_output)

#     except requests.exceptions.ConnectionError:
#         yield gr.update(value=""), gr.update(value="Error: Could not connect to the FastAPI server at `http://localhost:8000`. Please ensure `main.py` is running.")
#     except requests.exceptions.HTTPError as e:
#         yield gr.update(value=""), gr.update(value=f"Error from server: HTTP {e.response.status_code} - {e.response.text}\n\nPlease check the FastAPI server for details.")
#     except json.JSONDecodeError:
#         yield gr.update(value=""), gr.update(value=f"Error: Failed to decode JSON from FastAPI response. Raw text: {response.text}")
#     except Exception as e:
#         yield gr.update(value=""), gr.update(value=f"An unexpected error occurred: {str(e)}")

# with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container { max-width: 1200px; margin: auto; } .output-markdown { white-space: pre-wrap; }"
# ) as demo:
#     gr.Markdown("# 🌟 AI Resume Analyzer 🌟")
#     gr.Markdown(
#         "Upload a resume (PDF/DOCX) and paste a job description. "
#         "The app will analyze skill matches, suggest missing skills, "
#         "estimate proficiency levels, tailored to your selected interview focus."
#     )

#     with gr.Row(): # Use gr.Row() to create horizontal arrangement of columns
#         with gr.Column(scale=40): # Left Column (approx 40% width) - Increased slightly to accommodate job description
#             gr.Markdown("### Input Details") # Changed heading to be more general
#             resume_input = gr.File(label="Upload Resume (PDF/DOCX)", file_types=[".pdf", ".docx"], type="filepath")
#             file_type_choice = gr.Radio(
#                 ["PDF", "DOCX"], label="Select File Type", value="PDF"
#             )
#             interview_level_dropdown = gr.Dropdown(
#                 label="Select Interview Focus/Level",
#                 choices=[
#                     "General Match (Overall Fit)",
#                     "Junior/Entry-Level (Fundamentals & Learning Potential)",
#                     "Mid-Level (Solid Experience & Problem Solving)",
#                     "Senior/Lead (Leadership, Architecture & Mentorship)",
#                     "Technical Deep Dive (Algorithms & Data Structures)",
#                     "System Design (Scalability & Architecture)",
#                     "Behavioral/Culture Fit",
#                     "Product/Strategy Focus",
#                     "Domain-Specific (e.g., ML Engineering, Frontend, Backend)"
#                 ],
#                 value="General Match (Overall Fit)",
#                 interactive=True
#             )
#             job_description_textbox = gr.Textbox(label="Paste Job Description", lines=12, placeholder="Paste the job description here...")
#             submit_button = gr.Button("Submit", variant="primary")
            
#         with gr.Column(scale=60): # Right Column (approx 60% width)
#             gr.Markdown("### Analysis Results") # Changed heading for clarity
#             status_output = gr.Markdown(label="⏳ Status")
#             results_output = gr.Markdown(label="📄 Results")

#     # Connect the click event outside the column definitions but within the Blocks context
#     submit_button.click(
#         fn=analyze_resume,
#         inputs=[resume_input, file_type_choice, interview_level_dropdown, job_description_textbox],
#         outputs=[status_output, results_output]
#     )

# demo.launch(share=False)

import io
import json
import os
import requests

import docx
import gradio as gr
import pdfplumber

# For HTML export
import markdown # Import the markdown library

# --- API Endpoints ---
API_URL_ANALYZE = "http://localhost:8000/analyze"
API_URL_INTERVIEW_PREP = "http://localhost:8000/interview_prep"

# --- Global Variables for State Management ---
last_resume_text = ""
last_job_description = ""
last_matched_skills = []
last_missing_skills = []
last_proficiency_levels = {}
last_interview_level = ""
last_generated_markdown = "" # Stores the last generated markdown output

# --- Helper Functions for UI Logic ---

def generate_skill_analysis_markdown(matched_skills, missing_skills, proficiency_levels, interview_level) -> str:
    """
    Generates the Markdown string for the comprehensive skill analysis table.
    """
    formatted_output = f"## 📝 Resume Analysis Results\n\n"
    formatted_output += f"**Analysis Focus:** *{interview_level}*\n\n"

    all_skills = sorted(list(set(matched_skills + missing_skills + list(proficiency_levels.keys()))))
    
    if not all_skills:
        formatted_output += "No relevant skills found for analysis.\n"
    else:
        formatted_output += "### 📊 Comprehensive Skill Analysis:\n"
        formatted_output += "| Skill | Status | Proficiency Level |\n"
        formatted_output += "|---|---|---|\n"

        for skill in all_skills:
            status = ""
            if skill in matched_skills:
                status = "✅ Matched"
            elif skill in missing_skills:
                status = "⚠️ Missing"
            elif skill in proficiency_levels: 
                status = "➖ Mentioned"
            else: 
                status = "❓ Unknown"
            
            proficiency = proficiency_levels.get(skill, "N/A")
            formatted_output += f"| {skill} | {status} | {proficiency} |\n"
        formatted_output += "\n"
    return formatted_output

def generate_interview_prep_markdown(resume_text, job_description, interview_level) -> str:
    """
    Fetches interview preparation tips from the backend and formats them as Markdown.
    """
    if not resume_text or not job_description:
        return "Please run the full analysis first to generate interview preparation tips."

    try:
        data = {
            "resume_text": resume_text,
            "job_description": job_description,
            "interview_level": interview_level
        }
        response = requests.post(API_URL_INTERVIEW_PREP, data=data, timeout=180)
        response.raise_for_status()
        raw_output = response.json()
        
        tips_content = raw_output.get("tips", "Could not retrieve interview preparation tips.")
        
        formatted_output = f"## 🗣️ Interview Preparation Tips\n\n"
        formatted_output += f"**Focus:** *{interview_level}*\n\n"
        formatted_output += tips_content
        return formatted_output

    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the FastAPI server for interview tips. Ensure `main.py` is running."
    except requests.exceptions.Timeout:
        return "Error: Interview tips generation timed out. The AI model might be taking too long."
    except requests.exceptions.HTTPError as e:
        return f"Error from server for interview tips: HTTP {e.response.status_code} - {e.response.text}"
    except json.JSONDecodeError:
        return f"Error: Failed to decode JSON from FastAPI response for interview tips. Raw text: {response.text}"
    except Exception as e:
        return f"An unexpected error occurred while generating interview tips: {str(e)}"

def extract_resume_text_for_ui(file_path: str, file_type: str) -> str:
    """
    Extracts text from a resume file (PDF or DOCX) for use in the UI's
    internal storage and for sending to the interview prep endpoint.
    """
    try:
        if file_type == "PDF":
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"
                return text
        elif file_type == "DOCX":
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        return ""
    except Exception as e:
        print(f"Error extracting resume text in UI (for internal use): {e}")
        return ""

# --- New Function for HTML Export ---
def export_to_html(markdown_content: str):
    """
    Converts a Markdown string to an HTML file and returns the file path.
    """
    if not markdown_content:
        return None # No content to export

    try:
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Add a basic HTML wrapper for better viewing
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Analysis Report</title>
            <style>
                body {{ font-family: sans-serif; margin: 20px; line-height: 1.6; color: #333; }}
                h1, h2, h3 {{ color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 1em; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                pre {{ background-color: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                p {{ margin-bottom: 10px; }}
                ul, ol {{ margin-left: 20px; margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        temp_html_path = "analysis_report.html"
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        
        return temp_html_path
    except Exception as e:
        print(f"Error exporting to HTML: {e}")
        return None

# --- Main Gradio Event Handlers ---

def analyze_and_display(view_mode):
    """
    This function dynamically updates the results area based on the selected
    view mode, using the globally stored analysis results or by making a new API call.
    It's a generator function for streaming updates (e.g., "generating tips...").
    """
    global last_matched_skills, last_missing_skills, last_proficiency_levels, last_interview_level
    global last_resume_text, last_job_description, last_generated_markdown

    # Handle cases where analysis hasn't been run yet
    if not last_resume_text or not last_job_description:
        last_generated_markdown = "" # Clear content if no analysis
        return gr.update(value=""), gr.update(value="Please upload a resume, paste a job description, and run the analysis first."), gr.update(value=None) 

    if view_mode == "Comprehensive Skill Analysis":
        markdown_output = generate_skill_analysis_markdown(
            last_matched_skills, 
            last_missing_skills, 
            last_proficiency_levels, 
            last_interview_level
        )
        last_generated_markdown = markdown_output # Store for export
        # Immediately provide the HTML file path for download
        yield gr.update(value=""), gr.update(value=markdown_output), gr.update(value=export_to_html(last_generated_markdown))
    elif view_mode == "Interview Preparation Tips":
        yield gr.update(value="🔄 Generating interview tips... Please wait..."), gr.update(value=""), gr.update(value=None)

        markdown_output = generate_interview_prep_markdown(
            last_resume_text, 
            last_job_description, 
            last_interview_level
        )
        last_generated_markdown = markdown_output # Store for export
        # Immediately provide the HTML file path for download
        yield gr.update(value="Tips Generated!"), gr.update(value=markdown_output), gr.update(value=export_to_html(last_generated_markdown))


def run_full_analysis(resume_file, file_type_choice, interview_level, job_description):
    """
    Handles the initial full analysis process (file upload, text extraction,
    calling FastAPI analyze endpoint, storing results, and displaying initial view).
    It's a generator function for streaming updates.
    """
    global last_resume_text, last_job_description, last_matched_skills, last_missing_skills, last_proficiency_levels, last_interview_level
    global last_generated_markdown

    # --- Step 1: Clear previous results and set initial status ---
    last_generated_markdown = "" # Clear previous content
    # Always default to "Comprehensive Skill Analysis" view after initial run
    yield gr.update(value=""), gr.update(value=""), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)

    # --- Step 2: Basic Input Validation ---
    if resume_file is None or job_description.strip() == "":
        yield gr.update(value=""), gr.update(value="Please upload a resume and enter a job description."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
        return

    last_job_description = job_description
    last_interview_level = interview_level

    # --- Step 3: Extract Resume Text for Internal Storage ---
    try:
        last_resume_text = extract_resume_text_for_ui(resume_file.name, file_type_choice)
        if not last_resume_text:
             yield gr.update(value=""), gr.update(value="Could not extract text from resume. Please check file format."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
             return
    except Exception as e:
        yield gr.update(value=""), gr.update(value=f"Failed to read or parse resume file: {e}"), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
        return

    # --- Step 4: Prepare File for FastAPI Upload ---
    filename = resume_file.name
    if filename.endswith(".pdf"):
        content_type = "application/pdf"
    elif filename.endswith(".docx"):
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        yield gr.update(value=""), gr.update(value="Unsupported file type. Please upload a PDF or DOCX."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
        return

    file_bytes = None
    try:
        with open(filename, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        yield gr.update(value=""), gr.update(value=f"Failed to read uploaded file: {e}"), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
        return

    file_stream = io.BytesIO(file_bytes)

    files = {
        "resume": (os.path.basename(filename), file_stream, content_type)
    }
    data = {
        "job_description": job_description,
        "interview_level": interview_level
    }

    # --- Step 5: Call FastAPI Analysis Endpoint ---
    try:
        yield gr.update(value="🔄 Running skill analysis... Please wait..."), gr.update(value=""), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
        
        response = requests.post(API_URL_ANALYZE, files=files, data=data)
        response.raise_for_status()
        raw_output = response.json()

        if "error" in raw_output:
            yield gr.update(value=""), gr.update(value=f"**Backend Error:** {raw_output['error']}\n\nPlease check the FastAPI server logs."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
            return
        if "raw_response" in raw_output:
            yield gr.update(value=""), gr.update(value=f"**Could not parse JSON from AI model. Raw response:**\n```json\n{raw_output['raw_response']}\n```\n\n"), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
            return

        # --- Step 6: Store Parsed Results Globally ---
        all_skills_from_llm = raw_output.get("skills", [])
        last_matched_skills = [s["skill"] for s in all_skills_from_llm if s.get("matched")]
        last_proficiency_levels = {s["skill"]: s.get("proficiency", "N/A") for s in all_skills_from_llm if "skill" in s}
        last_missing_skills = raw_output.get("missing_skills", [])
        
        # --- Step 7: Display Initial Skill Analysis Output ---
        markdown_output = generate_skill_analysis_markdown(
            last_matched_skills, 
            last_missing_skills, 
            last_proficiency_levels, 
            last_interview_level
        )
        last_generated_markdown = markdown_output # Store for export
        
        # Yield final status, the markdown output, default view, and the HTML file for download
        yield gr.update(value="Analysis Complete!"), gr.update(value=markdown_output), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=export_to_html(last_generated_markdown))

    # --- Step 8: Error Handling for API Call ---
    except requests.exceptions.ConnectionError:
        yield gr.update(value=""), gr.update(value="Error: Could not connect to the FastAPI server at `http://localhost:8000`. Please ensure `main.py` is running."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
    except requests.exceptions.HTTPError as e:
        yield gr.update(value=""), gr.update(value=f"Error from server: HTTP {e.response.status_code} - {e.response.text}\n\nPlease check the FastAPI server for details."), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
    except json.JSONDecodeError:
        yield gr.update(value=""), gr.update(value=f"Error: Failed to decode JSON from FastAPI response. Raw text: {response.text}"), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)
    except Exception as e:
        yield gr.update(value=""), gr.update(value=f"An unexpected error occurred: {str(e)}"), gr.update(value="Comprehensive Skill Analysis"), gr.update(value=None)


# --- Gradio UI Definition ---
with gr.Blocks(
    theme=gr.themes.Soft(),
    css=".gradio-container { max-width: 1200px; margin: auto; } .output-markdown { white-space: pre-wrap; }"
) as demo:
    gr.Markdown("# 🌟 AI Resume Analyzer 🌟")
    gr.Markdown(
        "Upload a resume (PDF/DOCX) and paste a job description. "
        "The app will analyze skill matches, suggest missing skills, "
        "estimate proficiency levels, tailored to your selected interview focus. "
        "It can also generate interview preparation tips based on your resume and the job."
    )

    with gr.Row():
        with gr.Column(scale=40):
            gr.Markdown("### Input Details")
            resume_input = gr.File(
                label="Upload Resume (PDF/DOCX)",
                file_types=[".pdf", ".docx"],
                type="filepath",
                elem_id="resume_file_input"
            )
            file_type_choice = gr.Radio(
                ["PDF", "DOCX"],
                label="Select File Type",
                value="PDF",
                interactive=True
            )
            interview_level_dropdown = gr.Dropdown(
                label="Select Interview Focus/Level",
                choices=[
                    "General Match (Overall Fit)",
                    "Junior/Entry-Level (Fundamentals & Learning Potential)",
                    "Mid-Level (Solid Experience & Problem Solving)",
                    "Senior/Lead (Leadership, Architecture & Mentorship)",
                    "Technical Deep Dive (Algorithms & Data Structures)",
                    "System Design (Scalability & Architecture)",
                    "Behavioral/Culture Fit",
                    "Product/Strategy Focus",
                    "Domain-Specific (e.g., ML Engineering, Frontend, Backend)"
                ],
                value="General Match (Overall Fit)",
                interactive=True
            )
            job_description_textbox = gr.Textbox(
                label="Paste Job Description",
                lines=12,
                placeholder="Paste the job description here...",
                elem_id="job_desc_textbox"
            )
            submit_button = gr.Button("Analyze Resume", variant="primary")

        with gr.Column(scale=60):
            gr.Markdown("### Analysis Results")
            view_mode_radio = gr.Radio(
                ["Comprehensive Skill Analysis", "Interview Preparation Tips"],
                label="View Mode",
                value="Comprehensive Skill Analysis",
                interactive=True
            )
            
            status_output = gr.Markdown(label="⏳ Status")
            results_output = gr.Markdown(label="📄 Results")
            # Gradio File component for download, now for HTML
            html_download_button = gr.File(
                label="Download Report as HTML",
                type="filepath", # CORRECTED: Changed from "file" to "filepath"
                file_count="single",
                interactive=False # Make it non-interactive initially
            )


    # --- Event Handling ---
    submit_button.click(
        fn=run_full_analysis,
        inputs=[resume_input, file_type_choice, interview_level_dropdown, job_description_textbox],
        outputs=[status_output, results_output, view_mode_radio, html_download_button]
    )

    view_mode_radio.change(
        fn=analyze_and_display,
        inputs=[view_mode_radio],
        outputs=[status_output, results_output, html_download_button]
    )

# Launch the Gradio application
if __name__ == "__main__":
    demo.launch(share=False)