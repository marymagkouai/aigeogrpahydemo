import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Connection 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    
    # Let's try to automatically find the best available Flash model
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # We prefer the newest Flash models first
    if any("gemini-3-flash" in m for m in available_models):
        target_model = "gemini-3-flash"
    elif any("gemini-2.5-flash" in m for m in available_models):
        target_model = "gemini-2.5-flash"
    else:
        target_model = "gemini-1.5-flash" # Fallback

    model = genai.GenerativeModel(target_model)
    st.sidebar.success(f"Connected to: {target_model}")
except Exception as e:
    st.error("Connection Failed. Please check your API key in Secrets.")
    st.stop()

st.title("🌍 AI World Explorer")

# 2. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        res = model.generate_content("Ask a short, fun geography question.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("The AI couldn't generate a question.")
        st.exception(e)
        st.stop()

# 3. Interface 🖥️
st.info(st.session_state.question)
ans = st.text_input("What's your guess?", key="user_answer")

if st.button("Submit Answer"):
    if not ans:
        st.warning("Please type something!")
    else:
        try:
            prompt = f"Question: {st.session_state.question}\nUser answer: {ans}\nReturn ONLY JSON: {{\"is_correct\": bool, \"fact\": \"short fun fact\"}}"
            res = model.generate_content(prompt)
            
            # Clean and parse AI response
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
            st.error("Error processing answer.")
            st.exception(e)
