import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Init Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def call_gemini_for_rca(log_lines, file_name):
    prompt = f"""
I am analyzing server or application logs to identify potential root causes.
Here are some filtered log lines. Please summarize the issue, identify the likely root cause, and suggest next steps if possible.

Logs:
{chr(10).join(log_lines)}

Respond with your analysis in plain English.
"""

    # ✅ Fix: assign the response
    response = model.generate_content(prompt)

    # Save RCA output
    BASE_DIR = Path(__file__).resolve().parent.parent
    RCA_DIR = BASE_DIR / "outputs" / "rca"
    RCA_DIR.mkdir(parents=True, exist_ok=True)

    save_path = RCA_DIR / f"{file_name}_rca_output.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"[+] RCA saved to: outputs/rca/{file_name}_rca_output.txt")
