import streamlit as st
import PyPDF2
import google.generativeai as genai
import requests
import json
import re
import time


GEMINI_KEY = "AIzaSyAkvINm-FG4m-pUiwx7jX8_x4IvNDMZP68" 
SERPER_KEY = "7ea67648115d619e16691e54c4151b222754062e"

genai.configure(api_key=GEMINI_KEY)


model = None
working_model_name = ""
try:
    # Google se list maango jo models 'generateContent' support karte hain
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            working_model_name = m.name
            model = genai.GenerativeModel(working_model_name)
            break # Pehla working model milte hi ruk jao
except Exception as e:
    st.error(f"Engine Error: {e}")

# UI Design
st.set_page_config(page_title="Truth Layer Agent", layout="wide")
st.title("🛡️ The Fact-Check Agent: Truth Layer")
st.sidebar.success(f"Connected to: `{working_model_name}`")


def clean_and_parse_json(text):
    try:
        clean_text = text.replace('```json', '').replace('```', '').strip()
        json_match = re.search(r'[\{\[].*[\}\]]', clean_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group().replace("'", '"'))
        return None
    except:
        return None


uploaded_file = st.file_uploader("Choose a Marketing PDF", type="pdf")

if uploaded_file and model:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])
    
    if st.button("Start Automated Fact-Checking"):
        with st.spinner(f"Agent is auditing claims..."):
            try:
                # 1. Extract Claims
                extract_prompt = (
                    "Extract exactly 3 numerical or technical facts from this text. "
                    "Respond ONLY with a JSON array of strings. No extra talk. "
                    f"Text: {text[:2000]}"
                )
                
                response = model.generate_content(extract_prompt)
                raw_response = response.text.strip()
                claims = clean_and_parse_json(raw_response)
                
                # Backup if JSON fails
                if not claims:
                    claims = [l.strip("- ") for l in raw_response.split('\n') if len(l) > 15][:3]

                if claims and len(claims) > 0:
                    results = []
                    for claim in claims:
                        st.write(f"🔍 Checking: **{claim}**")
                        time.sleep(3) 
                        
                        # 2. Search
                        s_res = requests.post("https://google.serper.dev/search", 
                                             headers={'X-API-KEY': SERPER_KEY}, 
                                             json={"q": claim}).json()
                        snippet = s_res.get('organic', [{}])[0].get('snippet', "No info found")

                        # 3. Verify
                        v_prompt = f"Claim: {claim}\nWeb: {snippet}\nRespond JSON ONLY: {{'status': 'Verified/False', 'fact': 'msg'}}"
                        v_res = model.generate_content(v_prompt)
                        verdict = clean_and_parse_json(v_res.text)
                        
                        if verdict:
                            results.append({
                                "Claim": claim,
                                "Status": verdict.get('status', 'Unknown'),
                                "Evidence": verdict.get('fact', 'N/A')
                            })
                    
                    st.table(results)
                    st.success("✅ Complete! Record the video now.")
                else:
                    st.error("Could not find any facts. Check your PDF text.")
            except Exception as e:
                st.error(f"Error: {e}")