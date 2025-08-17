import streamlit as st

from agent_service import get_agent_response, create_session

if 'user_id' not in st.session_state:
    st.session_state.user_id = "tim"

if 'session_id' not in st.session_state:
    st.session_state.session_id = create_session(st.session_state.user_id)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(message['content'])
    else:
        with st.chat_message("assistant"):
            st.markdown(message['content'])

if user_input := st.chat_input("Ask a question about the weather in New York"):
    with st.chat_message("user"):
        st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        # Display a loading message while waiting for the response
        with st.spinner("Thinking..."):
            for item in get_agent_response(
                    user_input=user_input,
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id):
                for part in item['content'].get('parts', []):
                    if text := part.get('text'):
                        if part.get('thought'):
                            text = '**Thought:**\n\n' + text
                        st.markdown(text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": text})
