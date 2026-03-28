import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
st.set_page_config(page_title="Visual Explainer AI", page_icon="🖼️")

# Use your secret API Key from Streamlit Secrets or Sidebar
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # We enable 'google_search' so the AI can find real image links
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=[{"google_search": {}}] 
    )

    st.title("🖼️ Visual Concept Explainer")
    st.write("Enter a topic, and I'll explain it with plenty of visual aids.")

    # --- 2. USER INPUT ---
    topic = st.text_input("What do you want to learn about?", placeholder="e.g., How a Jet Engine works")
    detail_level = st.select_slider("Detail Level", options=["Simple", "Standard", "Deep Dive"])

    if st.button("Explain with Images"):
        if not topic:
            st.error("Please enter a topic first!")
        else:
            with st.spinner(f"Researching and finding images for '{topic}'..."):
                # --- 3. THE PROMPT ---
                # We tell the AI to use Markdown image syntax: ![description](url)
                prompt = f"""
                Explain the topic '{topic}' in a {detail_level} way.
                RULES:
                1. Break the explanation into 3-5 clear sections.
                2. IMPORTANT: For EVERY section, you MUST include a relevant image using Markdown: ![description](image_url).
                3. Use your Google Search tool to find actual, high-quality image URLs from educational sites or Wikipedia.
                4. Use bold headers and bullet points for readability.
                """
                
                try:
                    response = model.generate_content(prompt)
                    
                    # --- 4. DISPLAY OUTPUT ---
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

else:
    st.warning("Please enter your API Key in the sidebar to start.")
    st.info("You can get a free key at [aistudio.google.com](https://aistudio.google.com/)")

# --- 5. FOOTER ---
st.divider()
st.caption("Built for Visual Learners | Powered by Gemini 3 Series (2026)")