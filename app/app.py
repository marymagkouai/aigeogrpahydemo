import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Security 🔒
try:
    # .strip() handles any accidental spaces
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    
    # We use 'gemini-1.5-flash' which is the most compatible name
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup Error: Check your Streamlit Secrets!")
    st.stop()

st.title("🌍 AI World Explorer")

# 2. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        # Prompting the AI for the first question
        res = model.generate_content("Ask a short, fun geography question.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't start the game.")
        # This shows the specific error to help us debug
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
            # We ask for a simple JSON format to make parsing easier
            prompt = f"Question: {st.session_state.question}\nUser answer: {ans}\nIs it correct? Provide a fun fact. Return ONLY JSON: {{\"is_correct\": bool, \"fact\": str}}"
            res = model.generate_content(prompt)
            
            # Cleaning the text in case the AI adds markdown backticks
            clean_text = res.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_text)
            
            if data["is_correct"]:
                st.success(f"🥇 Correct! {data['fact']}")
                if st.button("Get New Question"):
                    # Clearing the state triggers a new question on refresh
                    for key in st.session_state.keys():
                        del st.session_state[key]
                    st.rerun()
            else:
                st.error(f"❌ Not quite. {data['fact']}")
        except Exception as e:
            st.error("There was an error processing the answer.")
            st.exception(e)
