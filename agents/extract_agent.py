import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))

print(" Loaded API Key:", os.getenv("OPENAI_API_KEY"))

# Set up OpenAI client
# Fetch environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# Azure-compatible OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url=f"{api_base}openai/deployments/{deployment_name}/",
    default_headers={"api-key": api_key},
    default_query={"api-version": api_version}
)

def build_prompt(summary_text):
    return f"""
You are a healthcare assistant AI.

Extract the following from the hospital discharge summary:
- Patient Name
- Diagnosis
- Medications prescribed
- Follow-up instructions
- Any missing or ambiguous information

Respond ONLY in the following JSON format:
{{
  "patient_name": "",
  "diagnosis": "",
  "medications": [],
  "follow_up": "",
  "missing_info": []
}}

Discharge Summary:
\"\"\"
{summary_text}
\"\"\"
"""
#ASk the LLM and return results
def extract_info(prompt):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a medical discharge assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=600
        )
        reply = response.choices[0].message.content
        return eval(reply) if reply.strip().startswith("{") else {"response": reply}
    except Exception as e:
        return {"error": str(e)}