import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Visual Link Explainer", page_icon="🔗")
st.title("🔗 Visual Concept Linker")
st.subheader("Deep-dive into topics with verified online sources")

# --- 2. SECURE API ACCESS ---
# Instead of a text input, we pull from Streamlit's hidden Vault
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 3. USER INTERFACE ---
topic = st.text_input("What would you like to explore?", placeholder="e.g., How a Jet Engine works")

if st.button("Generate Visual Guide"):
    if not topic:
        st.error("Please enter a topic!")
    else:
        with st.spinner(f"Researching '{topic}'..."):
            # Setup the search tool for grounding
            search_tool = types.Tool(google_search=types.GoogleSearch())
            
            prompt = f"""
            Explain the topic '{topic}' in 3 detailed sections for a visual learner.
            
            For EVERY section:
            1. Provide a clear explanation.
            2. Include 2+ clickable Markdown links [Title](URL) to high-quality diagrams, 
               educational images, or verified websites.
            3. Label links clearly (e.g., 'View Diagram of [Topic]').
            """

            # --- 4. EXECUTION WITH RETRY LOGIC (For 200+ users) ---
            success = False
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", 
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            tools=[search_tool],
                            temperature=0.7
                        )
                    )
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # Show sources if available
                    if response.candidates[0].grounding_metadata:
                        with st.expander("Verified Sources"):
                            st.write(response.candidates[0].grounding_metadata.search_entry_point.rendered_content, unsafe_allow_html=True)
                    
                    success = True
                    break # Exit the retry loop on success
                
                except Exception as e:
                    if "429" in str(e): # Overloaded error
                        st.warning(f"Server busy. Retrying in 5s... (Attempt {attempt+1}/3)")
                        time.sleep(5)
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if not success:
                st.error("The server is currently at capacity. Please try again in a minute.")

# --- 5. FOOTER ---
st.divider()
st.caption("Securely powered by Gemini 2.5 Flash-Lite")
