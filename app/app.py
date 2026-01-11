import streamlit as st
import google.generativeai as genai

# Try to initialize
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    
    # Just list the models - no complex generation yet
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ Connection successful! Found {len(model_list)} models.")
except Exception as e:
    st.error("❌ Still hitting a wall. Here is the raw error:")
    st.code(str(e))

import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Security 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # We add a specific transport to help the connection
    genai.configure(api_key=API_KEY, transport='grpc')
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup Error: Check your Streamlit Secrets!")
    st.stop()

st.title("🌍 AI World Explorer")

# 2. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        res = model.generate_content("Ask a short, fun geography question.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't start the game. Click 'Manage App' -> 'Logs' to see why.")
        st.exception(e)
        st.stop()

# 3. Interface 🖥️
st.info(st.session_state.question)
ans = st.text_input("What's your guess?", key="user_answer")

if st.button("Submit Answer"):
    if not ans:
        st.warning("Please type an answer first!")
    else:
        try:
            prompt = f"Question: {st.session_state.question}\nUser: {ans}\nCorrect? Return ONLY JSON: {{\"is_correct\": bool, \"fact\": str}}"
            res = model.generate_content(prompt)
            
            # Clean and parse JSON
            clean_text = res.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_text)
            
            if data["is_correct"]:
                st.success(f"🥇 Correct! {data['fact']}")
                if st.button("Next Question"):
                    del st.session_state.question
                    st.rerun()
            else:
                st.error(f"❌ Not quite. {data['fact']}")
        except Exception as e:
            st.error("Judging Error: The AI had trouble reading that.")
            st.exception(e)
