# AfterMedAI – Autonomous Post-Discharge Care Assistant

**AfterMedAI** is a **local-first, agentic AI app** designed to simplify post-hospital care. It autonomously analyzes discharge summaries, extracts key clinical details, flags missing information, and generates structured, patient-friendly care plans.

This project showcases how LLMs and prompt engineering can drive real-world healthcare impact.

---

##  Key Features

### Agentic AI Prompt Control
- Automatically generates optimized prompts
- Optional **custom prompt** entry 

### Care Plan Generation
- Creates detailed, structured Markdown-based care plans
- Personalized, readable output with daily schedule, FAQs, recovery timeline, red flags

### Real-Time Validation
- Flags missing or ambiguous information (e.g., dosage, follow-up)
- Helps ensure discharge summaries are clinically complete

### Chat-Enabled
- Ask follow-up questions to clarify medications or instructions
- Powered by LLM using session-based memory

### PDF Download
- Generates downloadable care plan PDF using `xhtml2pdf`
- No external binaries required

### Session Persistence
- Care plan and chat remain visible after actions
- “Start Over” button clears the session and resets the app


---

##  Agentic AI in Action

This app uses an **LLM-powered agent** that:
- Reads context-rich medical text
- Detects missing or ambiguous data (e.g., missing medication dosage)
- Plans and generates output that adapts based on document complexity
- Uses structured prompting or user-provided prompts (via toggle)

---

##  Folder Structure

```
care-coders/
├── .env                         # API keys and environment config
├── .gitignore
├── README.md
├── requirements.txt

├── agents/
│   ├── extract_agent.py         # LLM logic, prompt builder, and chatbot
│   ├── __init__.py
│   └── __pycache__/             # Compiled cache files

├── app/
│   ├── main.py                  # Streamlit app frontend
│   └── __init__.py

├── documentation/
│   └── Agentic AI workflow.png  # Agentic AI workflow explanation

├── examples/
│   ├── sample_discharge_pdf.pdf
│   └── sample_discharge_text.txt

├── output_examples/
│   ├── CarePlan1.pdf
│   └── CarePlan2.pdf

├── screenshots/                 # App UI screenshots
│   ├── AfterMedAI-Homepage.png
│   ├── Care-Plan-Generation.png
│   ├── Custom-Prompt-Toggle.png
│   ├── Discharge-Summary-from-input.png
│   ├── Downloadable-pdf.png
│   └── Session-reset.png

└── utils/
    └── logo.png                 # App logo


```

---

## Run Locally

### Clone the repo
git clone https://bitbucket.org/is_corp/care-coders.git
cd care-coders

### Install dependencies
pip install -r requirements.txt

### Set up your `.env`
Create a `.env` file based on `.env`:

OPENAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2023-12-01-preview


### Run the app
streamlit run app/main.py

---

## Why Local-First?

This app is designed as a **local-first agentic AI solution**:
- Runs entirely on your machine
- No cloud infrastructure required
- Can be extended to cloud if needed
- Ensures privacy for sensitive patient data

---

## Example Use Case

“A patient is discharged from a hospital with a complex summary. AfterMedAI reads the summary, flags that no follow-up date is mentioned, and generates a care plan reminding the patient to revisit their physician and continue their medications for 5 days.”

---

## Built With

- **OpenAI / Azure OpenAI** – LLM backbone
- **Streamlit** – For interactive UI
- **dotenv** – For API key management
- **xhtml2pdf** – For HTML-to-PDF generation
- **PyPDF2** – For reading PDF summaries
- **markdown** – For formatting care plans

---

## Authors

**Team:** Care Coders  
**Members:** Snehal Bandekar, Harshada Kothe, Samadhan Thube, Aditya Londhe, Jaideep Jahagirdhar, Siddharth Pimprikar  
**Project:** AfterMedAI  
**Hackathon:** Agentic AI Prompthon 
