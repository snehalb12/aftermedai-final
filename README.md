
# AfterMedAI – Autonomous Post-Discharge Care Assistant

**AfterMedAI** is a **local-first, agentic AI app** designed to simplify post-hospital care. It autonomously analyzes discharge summaries, extracts key clinical details, flags missing information, and generates structured, patient-friendly care plans.

This project showcases how LLMs and prompt engineering can drive real-world healthcare impact.

---

##  Key Features

-  **Discharge Summary Upload** – Upload hospital documents in `.txt` format.
-  **Autonomous Agent Behavior** – The app reasons through the input to identify missing info and generate care instructions.
-  **Prompt-Aware Design** – Toggle between auto-generated prompts and manual prompt input.
-  **Patient-Centered Output** – Outputs easy-to-understand care plans for follow-ups, medications, and recovery.

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
├── app/
│   └── main.py                  # Streamlit UI
├── agents/
│   └── extract_agent.py         # Core LLM logic and prompt generation
├── examples/
│   └── sample_discharge.txt     # Sample input
├── screenshots/
│   └── sample_output.png        # UI screenshot
├── .env                         # Template for secrets
├── .gitignore
├── requirements.txt
└── README.md
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

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
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

> “A patient is discharged from a hospital with a complex summary. AfterMedAI reads the summary, flags that no follow-up date is mentioned, and generates a care plan reminding the patient to revisit their physician and continue their medications for 5 days.”

---

## Built With

- **OpenAI / Azure OpenAI** – LLM backbone
- **LangChain** – Optional agent framework (modular)
- **Streamlit** – For interactive UI
- **dotenv** – For API key management


---

## Authors

**Team:** Care Coders - Snehal Bandekar, Samadhan Thube, Harshada Kothe, Aditya Londhe, Jaideep Jahagirdhar, Siddharth Pimprikar
**Project:** AfterMedAI  
**Hackathon:** Agentic AI Prompthon (2025)

