import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & API Configuration 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Setup Error: Check your Streamlit Secrets!")
    st.stop()

# 2. Reset Function 🔄
# This must be defined BEFORE the button that uses it
def get_new_question():
    if 'question' in st.session_state:
        del st.session_state.question
    # We also clear the response so the old feedback disappears
    if 'feedback' in st.session_state:
        del st.session_state.feedback

st.title("🌍 AI World Explorer")

# 3. Game Memory 🧠
# If 'question' is NOT in memory, ask the AI for one
if 'question' not in st.session_state:
    with st.spinner("Generating a new challenge..."):
        try:
            # Stricter prompt to prevent showing the answer
            prompt = "Ask a fun, short geography question. DO NOT include the answer."
            res = model.generate_content(prompt)
            st.session_state.question = res.text
        except Exception as e:
            st.error("Could not fetch a question.")
            st.stop()

# 4. Interface 🖥️
st.info(st.session_state.question)
user_ans = st.text_input("Your guess:", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Answer"):
        if user_ans:
            try:
                # Ask AI to judge the specific answer given
                judge_prompt = f"Q: {st.session_state.question}\nUser: {user_ans}\nReturn ONLY JSON: {{\"is_correct\": bool, \"fact\": str}}"
                res = model.generate_content(judge_prompt)
                
                # Clean and save feedback to session state
                clean_text = res.text.replace('```json', '').replace('```', '').strip()
                st.session_state.feedback = json.loads(clean_text)
            except:
                st.error("Error judging answer.")

with col2:
    # This button uses the 'on_click' callback to clear state BEFORE rerun
    st.button("Next Question 🆕", on_click=get_new_question)

# 5. Show Results 🥇
if 'feedback' in st.session_state:
    f = st.session_state.feedback
    if f["is_correct"]:
        st.success(f"🥇 Correct! {f['fact']}")
    else:
        st.error(f"❌ Not quite. {f['fact']}")
