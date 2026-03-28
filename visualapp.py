import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Visual Link Explainer", page_icon="🔗")
st.title("🔗 Visual Concept Linker")
st.subheader("Deep-dive into topics with verified online sources")

# --- 2. API KEY & CLIENT ---
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    # --- 3. INPUT ---
    topic = st.text_input("What would you like to explore?", placeholder="e.g., Quantum Computing Basics")
    
    if st.button("Generate Guide with Links"):
        if not topic:
            st.error("Please enter a topic!")
        else:
            with st.spinner(f"Searching for verified sources on {topic}..."):
                # We enable Google Search to get real-time URLs
                search_tool = types.Tool(google_search=types.GoogleSearch())
                
                # We specifically ask for LINKS instead of images
                prompt = f"""
                Explain the topic '{topic}' in 3 detailed sections.
                
                For EVERY section:
                1. Provide a clear, easy-to-understand explanation.
                2. Include at least 2 clickable Markdown links [Title](URL) to high-quality images, 
                   diagrams, or educational websites (like Wikipedia, NASA, or Khan Academy).
                3. Label the links clearly, e.g., 'View Diagram of [Topic]' or 'Read more at [Site]'.
                """
                
                try:
                    # Using Flash-Lite for better free-tier scaling for 200 users
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", 
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[search_tool],
                            temperature=0.7 # Keeps the explanation stable
                        )
                    )
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # Optional: Show the Google Search queries used
                    if response.candidates[0].grounding_metadata:
                        with st.expander("Sources & Search Queries"):
                            st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content, unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
                    st.info("Tip: If you see 'Resource Exhausted', wait 30 seconds and try again.")
else:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start.")
