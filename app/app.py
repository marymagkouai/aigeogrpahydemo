import streamlit as st
import google.generativeai as genai
import json

# 1. Setup & Connection 🔒
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    
    # Try the latest Gemini 3 model first
    # If that fails, it will use the stable 2.5 version
    try:
        model_name = "gemini-3-flash-preview"
        model = genai.GenerativeModel(model_name)
        # Test if this model name works
        model.generate_content("test", generation_config={"max_output_tokens": 1})
    except:
        model_name = "gemini-2.5-flash"
        model = genai.GenerativeModel(model_name)

    st.sidebar.success(f"Using Model: {model_name}")
except Exception as e:
    st.error("Connection Failed. Check your API key in Secrets.")
    st.stop()

st.title("🌍 AI World Explorer")

# 2. Game Memory 🧠
if 'question' not in st.session_state:
    try:
        res = model.generate_content("Ask a short, fun geography question.")
        st.session_state.question = res.text
    except Exception as e:
        st.error("AI Generation Error")
        st.exception(e)
        st.stop()

# 3. Interface 🖥️
st.info(st.session_state.question)
ans = st.text_input("What's your guess?", key="user_answer")

if st.button("Submit Answer"):
    if not ans:
        st.warning("Please type an answer!")
    else:
        try:
            prompt = f"Question: {st.session_state.question}\nUser: {ans}\nReturn ONLY JSON: {{\"is_correct\": bool, \"fact\": \"short fact\"}}"
            res = model.generate_content(prompt)
            
            # Clean and parse JSON
            clean_text = res.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_text)
            
            if data["is_correct"]:
                st.success(f"🥇 Correct! {data['fact']}")
                st.button("Next Question", on_click=lambda: st.session_state.pop('question'))
            else:
                st.error(f"❌ Not quite. {data['fact']}")
        except Exception as e:
            st.error("Processing Error")
            st.exception(e)
