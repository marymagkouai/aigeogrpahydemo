import streamlit as st
import google.generativeai as genai
import json

# 1. Ρύθμιση και Σύνδεση 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    # Χρήση του μοντέλου gemini-2.0-flash για το 2026
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error("Σφάλμα Ρύθμισης: Ελέγξτε το API Key στα Secrets!")
    st.stop()

# 2. Λειτουργία Επαναφοράς 🔄
def get_new_question():
    # Διαγράφουμε την ερώτηση και την απάντηση από τη μνήμη
    keys_to_reset = ['question', 'feedback', 'user_input']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

st.title("🌍 AI Παγκόσμιος Εξερευνητής")

# 3. Μνήμη Παιχνιδιού 🧠
if 'question' not in st.session_state:
    try:
        # Οδηγία για ερώτηση στα Ελληνικά χωρίς την απάντηση
        res = model.generate_content("Κάνε μια σύντομη και διασκεδαστική ερώτηση γεωγραφίας στα Ελληνικά. ΜΗΝ συμπεριλάβεις την απάντηση.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("Η AI δεν μπόρεσε να δημιουργήσει ερώτηση.")
        st.stop()

# 4. Περιβάλλον Χρήστη 🖥️
st.info(st.session_state.question)
user_ans = st.text_input("Η απάντησή σου:", key="user_input")

col1, col2 = st.columns(2)

with col1:
    if st.button("Υποβολή Απάντησης"):
        if user_ans:
            try:
                # Ζητάμε από την AI να κρίνει την απάντηση και να δώσει τη σωστή
                prompt = f"""
                Ερώτηση: {st.session_state.question}
                Απάντηση Χρήστη: {user_ans}
                Επέστρεψε ΜΟΝΟ JSON στα Ελληνικά: 
                {{"is_correct": bool, "correct_answer": "string", "fact": "string"}}
                """
                res = model.generate_content(prompt)
                clean_
