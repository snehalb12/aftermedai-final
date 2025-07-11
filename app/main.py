import sys
import os

# Adding the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import streamlit for deployment
import streamlit as st
from agents.extract_agent import build_prompt, extract_info

st.set_page_config(page_title="AfterMedAI", page_icon=" ", layout="centered")

st.title("AfterMedAI")
st.subheader("Autonomous Post-Discharge Care Planner")

uploaded_file = st.file_uploader("Upload a discharge summary (.txt)", type=["txt"])

if uploaded_file:
    summary_text = uploaded_file.read().decode("utf-8")

    st.markdown("Discharge Summary:")
    st.text_area("Summary Content", summary_text, height=300, disabled=True)

    # Add prompt toggle
    use_custom_prompt = st.checkbox(" Customize the prompt")

    if use_custom_prompt:
        custom_prompt = st.text_area("Enter your custom prompt", build_prompt(summary_text), height=300)
        final_prompt = custom_prompt
    else:
        final_prompt = build_prompt(summary_text)

    with st.expander("View Final Prompt Sent to the Agent"):
        st.code(final_prompt, language="markdown")

    if st.button("Generate Care Plan"):
        with st.spinner("Generating care plan ...."):
            result = extract_info(final_prompt)

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.markdown("Generated Care Plan:")
                st.json(result)
