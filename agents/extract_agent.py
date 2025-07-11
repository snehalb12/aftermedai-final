import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','.env')))

api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = OpenAI(
    api_key=api_key,
    base_url=f"{api_base}openai/deployments/{deployment_name}/",
    default_headers={"api-key":api_key},
    default_query={"api-version":api_version}
)

# Create LLM prompt to extract important information and generate a personalized post health care plan
def build_prompt(discharge_text):
    return f"""
You are a post-discharge care assistant for patients.
Your job has two parts:
1️. First, carefully extract the important details from the discharge text, including:
- Name of the patient
- Name of the doctor
- Diagnosis
- Medications (name, dose, frequency)
- Follow-up date
- Activity restrictions
- Diet instructions
- Warning signs
- Any other important instructions

2️. Then, using those details, write a **personalized, clear, and supportive post-discharge plan** for the patient.
The plan must include:
- A short summary of the patient’s condition and treatment in plain language
- A clear daily care plan with simple steps (morning, afternoon, evening as required)
- 3–4 common FAQs with helpful answers
- A recovery timeline in simple language
- Clear warning signs (red flags) for when to call the doctor immediately
- Gentle behavior tips or reminders that can help recovery

The tone must be warm, caring, and easy to understand for a non-medical person.
Format the entire plan in **well-structured Markdown** with headings, bullet points, and short paragraphs.
Just output the final care plan in plain Markdown.
Do NOT add any extra explanations or commentary — output only the final care plan.

Discharge Document:
***
{discharge_text}
***
"""

    
def extract_info(summary_text, custom_prompt=None):
    prompt = custom_prompt if custom_prompt else build_prompt(summary_text)

    # Call OpenAI/Azure OpenAI API
    response = client.chat.completions.create(
        model=deployment_name,  # Azure deployment name
        messages=[
            {"role":"system","content":"You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=2000
    )

    care_plan = response.choices[0].message.content

    # Real-time validation
    flags = []
    summary_lower = summary_text.lower()
    if "follow-up" not in summary_lower:
        flags.append("Missing follow-up instructions")
    if "mg" not in summary_lower and "dosage" not in summary_lower:
        flags.append("Missing medication dosage")
    if "medication" not in summary_lower and "prescribed" not in summary_lower:
        flags.append("No clear medication details found")

    return {
        "care_plan": care_plan,
        "flags": flags
    }

# Send the user question to LLM for Q&A using input as the extracted information ad previous chat history
def chatbot(extracted_info, chat_history):
    try:
        messages=[
            {"role":"system","content":"You are a helpful medical assistant."},
            {"role":"user","content":f"Here is the extracted patient info: {extracted_info}. Answer the user's question using this info."}
        ]
        messages.extend(chat_history)
        response = client.chat.completions.create(
            messages=messages,
            model=deployment_name,
            temperature=0.4,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"



