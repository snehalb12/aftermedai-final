import sys
import os
import base64
import streamlit as st

# Allow importing from the parent directory (for agents/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from agents.extract_agent import build_prompt, extract_info, chatbot
from xhtml2pdf import pisa
import io
import markdown
from PyPDF2 import PdfReader

# Streamlit set up
st.set_page_config(page_title="AfterMedAI",page_icon="🏥",layout="wide")

# Convert logo to base 64
def get_base_64(path):
    with open(path,"rb") as f:
        return base64.b64encode(f.read()).decode()

script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir,"..","utils","logo.png")
logo_base_64 = get_base_64(logo_path)

# Sidebar Setup
with st.sidebar:
    st.markdown(
        f"""
        <div style='text-align: centre;'>
            <img src='data:image/png;base64,{logo_base_64}'width='150'>
            <br>
            <h2 style='color: #1f4e79;'>AfterMedAI</h2>
        </div>            
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:14px;color:#666;'>Your trusted autonomous care plan assistant.</p>",
        unsafe_allow_html=True
    )    

# Initialize session state
if "extracted_info" not in st.session_state:
    st.session_state["extracted_info"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "discharge_text" not in st.session_state:
    st.session_state["discharge_text"] = ""

def save_pdf_with_pisa(html_content):
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=result)
    return result.getvalue() if not pisa_status.err else None

# UI Title
st.title("AfterMedAI - Care Plan Generator")

# File upload & prompt input (only if not already processed)
if not st.session_state["extracted_info"]:
    uploaded_file = st.file_uploader("Upload Discharge Summary (.pdf or .txt)", type=["pdf", "txt"])

    if uploaded_file:
        # Extract text
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            discharge_text = ""
            for page in pdf_reader.pages:
                discharge_text += page.extract_text()
        elif uploaded_file.type == "text/plain":
            discharge_text = uploaded_file.getvalue().decode("utf-8")
        else:
            st.error("Unsupported file type.")
            st.stop()

        # Store once in session state
        st.session_state["discharge_text"] = discharge_text

        st.markdown("Discharge Summary Preview")
        st.text_area("Document Content", discharge_text, height=300, disabled=True)

        # Prompt customization
        enable_custom_prompt = st.checkbox("Customize the prompt")
        if enable_custom_prompt:
            custom_prompt = st.text_area("Enter your custom prompt", build_prompt(discharge_text), height=300)
            final_prompt = custom_prompt
        else:
            final_prompt = build_prompt(discharge_text)

        if st.button("Generate Care Plan"):
            with st.spinner("Generating care plan..."):
                result = extract_info(final_prompt)
                st.session_state["extracted_info"] = result
                st.session_state["chat_history"] = []

# Show care plan + download + chat after generation
if st.session_state["extracted_info"]:
    st.markdown("Generated Care Plan")
    st.markdown(st.session_state["extracted_info"]["care_plan"])

    html_content = markdown.markdown(st.session_state["extracted_info"]["care_plan"])
    pdf_data = save_pdf_with_pisa(html_content)

    if pdf_data:
        st.download_button(
            label="Download Care Plan as PDF",
            data=pdf_data,
            file_name="CarePlan.pdf",
            mime="application/pdf"
        )
    else:
        st.error("PDF generation failed.")

    # Follow-up Chat
    st.subheader("Ask a Follow-up Question")
    question = st.text_input("Your question:")

    if st.button("Ask"):
        if question:
            st.session_state["chat_history"].append({"role": "user", "content": question})
            reply = chatbot(
                st.session_state["extracted_info"]["care_plan"],
                st.session_state["chat_history"]
            )
            st.session_state["chat_history"].append({"role": "assistant", "content": reply})

    for msg in st.session_state["chat_history"]:
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

    # Reset button
    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()