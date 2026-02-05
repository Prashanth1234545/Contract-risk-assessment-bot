import streamlit as st
import google.generativeai as genai
import pdfplumber
from fpdf import FPDF

# 1. SETUP FREE AI
# Replace the text below with your actual API key from Step 1
genai.configure(api_key="AIzaSyCccfC5kj1Y8OIMrsn535OoYbwuKZltJL4")
model = genai.GenerativeModel('gemini-2.0-flash') # Using the latest 2026 model

st.set_page_config(page_title="Contract Risk Bot", page_icon="⚖️")
st.title("⚖️ Contract Risk Assessment Bot")
st.info("HCL Hackathon Submission - Free Edition")

# 2. FILE UPLOADER
uploaded_file = st.file_uploader("Upload Contract (PDF)", type=["pdf"])

if uploaded_file:
    # Extract Text from PDF
    with pdfplumber.open(uploaded_file) as pdf:
        contract_text = "".join([page.extract_text() for page in pdf.pages])
    
    st.success("Contract loaded successfully!")

    if st.button("Analyze Risk"):
        with st.spinner("AI is evaluating legal risks..."):
            # The prompt designed to meet HCL requirements
            prompt = f"""
            Analyze this contract text: {contract_text[:8000]}
            
            Provide a detailed report in English and Hindi including:
            1. Extract Parties, Effective Date, and Jurisdiction.
            2. Provide a 'Composite Risk Score' (1-10).
            3. List risks in Indemnity, Penalties, and Unilateral Termination.
            4. Provide plain-language explanations for complex legal terms.
            """
            
            try:
                response = model.generate_content(prompt)
                st.session_state['analysis'] = response.text
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

    # 3. PDF EXPORT (Mandatory HCL Requirement)
    if 'analysis' in st.session_state:
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            # Basic cleanup for PDF encoding
            clean_text = st.session_state['analysis'].encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 10, clean_text)
            
            st.download_button(
                label="Download Risk Report",
                data=pdf.output(dest='S'),
                file_name="legal_risk_report.pdf",
                mime="application/pdf"
            )
