import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Connection 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    # Using the standard stable model for 2026
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Setup Error: Check your Streamlit Secrets!")
    st.stop()

# 2. Reset Function 🔄
def get_new_question():
    keys_to_reset = ['question', 'feedback', 'user_input']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

st.title("🌍 AI World Explorer")

# 3. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        # Prompt for just the question
        res = model.generate_content("Ask a fun, short geography question. DO NOT include the answer.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't generate a question.")
        st.stop()

# 4. Interface 🖥️
st.info(st.session_state.question)
# Use a key to handle clearing the input later
user_ans = st.text_input("Your guess:", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Answer"):
        if user_ans:
            try:
                # Updated judge prompt to include the correct answer
                prompt = f"""
                Q: {st.session_state.question}
                User: {user_ans}
                Return ONLY JSON: 
                {{"is_correct": bool, "correct_answer": "string", "fact": "string"}}
                """
                res = model.generate_content(prompt)
                clean_text = res.text.replace('```json', '').replace('```', '').strip()
                st.session_state.feedback = json.loads(clean_text)
            except:
                st.error("Error judging answer.")

with col2:
    st.button("Next Question 🆕", on_click=get_new_question)

# 5. The "Reveal" Box 🥇
# This only appears AFTER submission
if 'feedback' in st.session_state:
    f = st.session_state.feedback
    
    if f["is_correct"]:
        st.success(f"🥇 Correct! The answer was indeed {f['correct_answer']}.")
    else:
        # We show the correct answer here because the user was wrong
        st.error(f"❌ Not quite. The correct answer was: **{f['correct_answer']}**")
    
    st.info(f"💡 **Did you know?** {f['fact']}")
