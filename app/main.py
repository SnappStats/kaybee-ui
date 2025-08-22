import streamlit as st
from streamlit_extras.bottom_container import bottom
import streamlit_mermaid as stmd
from agent_service import get_agent_response, create_session
from agraph import get_agraph

AI_AVATAR = 'app/splash.png'
USER_AVATAR = '🧑'

if 'user_id' not in st.session_state:
    st.session_state.user_id = "tim"

if 'session_id' not in st.session_state:
    company = 'Apple'
    st.session_state.session_id = create_session(
            st.session_state.user_id, company)

if 'messages' not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title='Kaybee', page_icon='app/splash.png')
st.logo('app/bee.png', size='large', link=None)
title_col1, title_col2 = st.columns([1, 3], gap='small')
with title_col1:
    st.image('app/bee.png', width=200)
with title_col2:
    st.title('Tribal Knowledge Base')

column1, column2 = st.columns([1,2])
with column1:
    with st.container(height=500):
        for message in st.session_state.messages:
            if message['role'] == 'user':
                with st.chat_message("user", avatar=USER_AVATAR):
                    st.markdown(message['content'])
            else:
                with st.chat_message("assistant", avatar=AI_AVATAR):
                    st.markdown(message['content'])

        if st.session_state.get('user_input'):
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(st.session_state.user_input.text)
                st.session_state.messages.append(
                    {"role": "user", "content": st.session_state.user_input.text})
            with st.chat_message("assistant", avatar=AI_AVATAR):
                # Display a loading message while waiting for the response
                with st.spinner("Thinking..."):
                    agent_response = get_agent_response(
                            user_input=st.session_state.user_input.text,
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id)
                    if agent_response.status_code != 200:
                        st.error(agent_response.json())
                    else:
                        for item in agent_response.json():
                            for part in item['content'].get('parts', []):
                                if text := part.get('text'):
                                    if part.get('thought'):
                                        text = '**Thought:**\n\n' + text
                                        st.caption(text)
                                    else:
                                        st.markdown(text)
                                        st.session_state.messages.append(
                                            {"role": "assistant", "content": text})
with column2:
    with st.container():
        if agraph_clicked := get_agraph():
            agraph_clicked
        #stmd.st_mermaid('''
        #graph TD;
        #    A[User] -->|Ask question| B[Kaybee Agent];
        #    B -->|Fetch data| C[Weather API];
        #    C -->|Return data| B;
        #    B -->|Respond| A;
        #''')

with bottom():
    st.chat_input(
            'Teach me something...',
            key='user_input',
            accept_file=True,
            file_type=['pdf'])
