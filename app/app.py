import streamlit as st
import google.generativeai as genai
import json

# 🔒 Securely get your API key from Streamlit's hidden secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🌍 AI World Explorer")

# Game Memory
if 'question' not in st.session_state:
    res = model.generate_content("Ask a short, fun geography question.")
    st.session_state.question = res.text

# Interface
st.info(st.session_state.question)
ans = st.text_input("What's your guess?")

if st.button("Submit"):
    prompt = f"Question: {st.session_state.question}\nUser: {ans}\nCorrect? JSON: {{\"is_correct\": bool, \"fact\": str}}"
    res = model.generate_content(prompt)
    clean_text = res.text.replace('```json', '').replace('```', '').strip()
    data = json.loads(clean_text)
    
    if data["is_correct"]:
        st.success(f"🥇 Correct! {data['fact']}")
    else:
        st.error(f"❌ Not quite. {data['fact']}")
