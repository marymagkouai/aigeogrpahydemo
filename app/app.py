import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Connection 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    
    # Using 'gemini-2.0-flash' - the stable standard for 2026
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Setup Error: Check your Streamlit Secrets!")
    st.stop()

# 2. Reset Function 🔄
def get_new_question():
    if 'question' in st.session_state:
        del st.session_state.question
    if 'feedback' in st.session_state:
        del st.session_state.feedback

st.title("🌍 AI World Explorer")

# 3. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        # Prompting for ONLY a question
        res = model.generate_content("Ask a fun, short geography question. DO NOT include the answer.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't generate a question.")
        st.code(str(e)) # This helps us see the EXACT error if it fails
        st.stop()

# 4. Interface 🖥️
st.info(st.session_state.question)
user_ans = st.text_input("Your guess:", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Answer"):
        if user_ans:
            try:
                # Prompting for judging the answer
                prompt = f"Q: {st.session_state.question}\nUser: {user_ans}\nReturn ONLY JSON: {{\"is_correct\": bool, \"fact\": \"short fact\"}}"
                res = model.generate_content(prompt)
                clean_text = res.text.replace('```json', '').replace('```', '').strip()
                st.session_state.feedback = json.loads(clean_text)
            except:
                st.error("Error judging answer.")

with col2:
    st.button("Next Question 🆕", on_click=get_new_question)

# 5. Show Results 🥇
if 'feedback' in st.session_state:
    f = st.session_state.feedback
    if f["is_correct"]:
        st.success(f"🥇 Correct! {f['fact']}")
    else:
        st.error(f"❌ Not quite. {f['fact']}")
