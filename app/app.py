import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Connection 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    # Using the stable Gemini 2.0 Flash model
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Error: Please check your API key in Streamlit Secrets.")
    st.stop()

# 2. Reset Function 🔄
def reset_game():
    # Clear memory so the next run triggers a new question
    for key in ['question', 'feedback', 'user_input']:
        if key in st.session_state:
            del st.session_state[key]

st.title("🌍 AI World Explorer")

# 3. Game Memory (The Question) 🧠
if 'question' not in st.session_state:
    try:
        # Prompting specifically for Greek content
        res = model.generate_content("Ask a fun, short geography question in GREEK. DO NOT include the answer.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't generate a question.")
        st.stop()

# 4. Interface 🖥️
st.info(st.session_state.question)
user_ans = st.text_input("Η απάντησή σου (Your guess):", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Submit Answer"):
        if user_ans:
            try:
                # We force the JSON keys to be Greek-friendly to keep the AI in "Greek mode"
                prompt = f"""
                Question: {st.session_state.question}
                User Answer: {user_ans}
                Respond ONLY with a JSON object in GREEK using this structure:
                {{"einai_sosto": bool, "sosti_apantisi": "string", "geografiko_gegonos": "string"}}
                """
                res = model.generate_content(prompt)
                clean_text = res.text.replace('```json', '').replace('```', '').strip()
                st.session_state.feedback = json.loads(clean_text)
            except:
                st.error("Error processing the answer.")

with col2:
    # This button uses the callback to reset memory before the app reruns
    st.button("Next Question 🆕", on_click=reset_game)

# 5. The Reveal Box 🥇
if 'feedback' in st.session_state:
    f = st.session_state.feedback
    
    # We use the Greek keys we defined in the prompt
    if f["einai_sosto"]:
        st.success(f"🥇 Σωστά! (Correct!) The answer was: {f['sosti_apantisi']}")
    else:
        st.error(f"❌ Όχι ακριβώς. (Not quite.) The correct answer was: **{f['sosti_apantisi']}**")
    
    st.info(f"💡 **Το ήξερες; (Did you know?)** {f['geografiko_gegonos']}")
