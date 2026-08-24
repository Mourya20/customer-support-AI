"""Streamlit app entrypoint for the customer support AI MVP."""

import streamlit as st

from src.pipeline import SupportPipeline

st.set_page_config(page_title="Customer Support AI", page_icon="🤖")
st.title("Customer Support AI Employee")
st.caption("MVP: Classification → Retrieval → Grounded Answer / Escalation")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pipeline" not in st.session_state:
    st.session_state.pipeline = SupportPipeline()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask a support question...")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    result = st.session_state.pipeline.handle_query(user_query)

    if result["escalate"]:
        assistant_message = (
            "⚠️ **ESCALATION REQUIRED**\n\n"
            f"**Reason:** {result['escalation_reason']}\n\n"
            "**Recommended action:** Route this case to a human support agent.\n\n"
            f"**Category:** {result['category']}\n"
            f"**Confidence:** {result['classification_confidence']}"
        )
    else:
        sources = ", ".join(result["sources"])
        assistant_message = (
            f"{result['answer']}\n\n"
            f"**Category:** {result['category']}\n"
            f"**Confidence:** {result['classification_confidence']}\n"
            f"**Sources:** {sources}"
        )

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
