import streamlit as st
import google.generativeai as genai

st.title("🔑 API Connection Test")

try:
    # Use the secret
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Try to list models (this is the simplest 'handshake' test)
    models = genai.list_models()
    st.success("✅ Connection Successful! Found models:")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            st.write(f"- {m.name}")
            
except Exception as e:
    st.error(f"❌ Connection Failed!")
    st.code(str(e)) # This will show the RAW error from Google
