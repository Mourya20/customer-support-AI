"""Streamlit app entrypoint for the customer support AI MVP."""

import streamlit as st

st.set_page_config(page_title="Customer Support AI", page_icon="🤖")
st.title("Customer Support AI Employee")
st.caption("MVP demo chat interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask a support question...")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    placeholder_response = (
        "Pipeline integration is coming next. This UI will show category, confidence, "
        "grounded answer, and escalation reason when needed."
    )

    st.session_state.messages.append({"role": "assistant", "content": placeholder_response})
    with st.chat_message("assistant"):
        st.markdown(placeholder_response)
