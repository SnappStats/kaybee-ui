import streamlit as st
import streamlit_mermaid as stmd
from agent_service import get_agent_response, create_session

if 'user_id' not in st.session_state:
    st.session_state.user_id = "tim"

if 'session_id' not in st.session_state:
    company = 'Apple'
    st.session_state.session_id = create_session(
            st.session_state.user_id, company)

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title('Kaybee')
st.caption('Tribal knowledge agent')

column1, column2 = st.columns(2)
with column1:
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
with column2:
    stmd.st_mermaid('''
    graph TD;
        A[User] -->|Ask question| B[Kaybee Agent];
        B -->|Fetch data| C[Weather API];
        C -->|Return data| B;
        B -->|Respond| A;
    ''')
