import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# --- Safety Check ---
if "GOOGLE_API_KEY" in st.secrets:
    raw_key = st.secrets["GOOGLE_API_KEY"]
    # Show only the first 4 and last 3 characters for safety
    st.write(f"🔍 Key Preview: `{raw_key[:4]}...{raw_key[-3:]}`")
    st.write(f"📏 Key Length: {len(raw_key)} characters")
else:
    st.error("❌ The secret 'GOOGLE_API_KEY' was not found!")
# --------------------

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
