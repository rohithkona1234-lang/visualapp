import streamlit as st
from google import genai
from google.genai import types

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Visual Explainer AI", page_icon="🖼️")

st.title("🖼️ Visual Concept Explainer")
st.write("Explain any topic with real-world images and diagrams.")

# --- 2. AUTHENTICATION ---
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    # Initialize the new 2026 Client
    client = genai.Client(api_key=api_key)
    
    # --- 3. USER INPUT ---
    topic = st.text_input("What do you want to learn about?", placeholder="e.g., The Water Cycle")
    
    if st.button("Explain with Images"):
        if not topic:
            st.error("Please enter a topic!")
        else:
            with st.spinner(f"Researching '{topic}'..."):
                # Use 'google_search' tool to ground the AI in real data and images
                search_tool = types.Tool(google_search=types.GoogleSearch())
                
                prompt = f"""
                Explain '{topic}' for a visual learner.
                Use 3-5 sections. 
                CRITICAL: Every section MUST include a relevant image using Markdown: ![description](url).
                Use the Google Search tool to find real educational image URLs.
                """
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", # Best for fast tool-use
                        contents=prompt,
                        config=types.GenerateContentConfig(tools=[search_tool])
                    )
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("👈 Please enter your API Key in the sidebar to begin.")
