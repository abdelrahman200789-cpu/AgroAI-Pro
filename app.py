from pathlib import Path
import streamlit as st
from agro_engine import search_knowledge

st.set_page_config(
    page_title="AgroAI Pro | Knowledge Chat",
    page_icon="🌱",
    layout="centered",
)

st.markdown("""
<style>

/* Make chat messages readable */
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    color: #1f2937 !important;
    border: 1px solid #dce7df;
    border-radius: 14px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] div {
    color: #1f2937 !important;
}

/* Chat input */
[data-testid="stChatInput"] textarea {
    color: #1f2937 !important;
    background-color: #ffffff !important;
    caret-color: #27734e;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #66756c !important;
    opacity: 1;
}

</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent

st.markdown("""
<div class="hero">
<h1>🌿 AgroAI Pro</h1>
<p>Your agricultural knowledge assistant</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Ask about irrigation, soil pH, crop planning, plant diseases, "
    "pest management, or agricultural sensors."
)

with st.sidebar:
    st.title("🌱 AgroAI Pro")
    st.write("Information Retrieval using TF-IDF and Cosine Similarity.")
    st.caption("Answers are retrieved from local agricultural notes.")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

suggestions = [
    # Soil and nutrients
    "How can I check soil pH?",
    "How does soil pH affect plant growth?",
    "How can I improve soil quality?",

    # Irrigation
    "How often should I irrigate crops?",
    "How can I check soil moisture?",
    "What causes overwatering in crops?",

    # Plant diseases
    "How do I scout plants for disease?",
    "What are common signs of plant disease?",
    "How can I monitor disease spread in a field?",

    # Pests
    "What is integrated pest management?",
    "How can I monitor crop pests?",

    # Crop planning
    "How do I choose a suitable crop?",
    "What factors affect crop planning?",
    "Why is crop rotation important?",

    # Sensors and data
    "How can I improve sensor data quality?",
    "How can I check if a sensor is calibrated?",

]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            with st.expander("Sources used"):
                for source in message["sources"]:
                    st.markdown(f"**{source['title']}**")
                    st.write(source["content"])
                    st.caption(
                        f"Relevance: {source['score_percent']}% | "
                        f"File: {source['file']}"
                    )

if not st.session_state.messages:
    st.markdown("**Try asking:**")
    cols = st.columns(2)

    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion, key=f"suggestion_{i}"):
            st.session_state.pending_question = suggestion
            st.rerun()

question = st.chat_input("Ask an agricultural question...")

if not question and "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            results = search_knowledge(question)

            if results:
                best = results[0]
                answer = (
                    f"### {best['title']}\n\n"
                    f"{best['content']}\n\n"
                    f"Source: `{best['file']}`"
                )
                st.markdown(answer)

                with st.expander("Related sources"):
                    for result in results[1:3]:
                        st.markdown(f"**{result['title']}**")
                        st.write(result["content"])
            else:
                st.info("No matching information was found.")

            st.session_state.messages.append({
                "role": "user",
                "content": question,
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer if results else "No matching information was found.",
                "sources": results[:3],
            })

        except Exception as error:
            st.error(f"Error: {error}")
            st.exception(error)