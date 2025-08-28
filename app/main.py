import os
import streamlit as st
import streamlit_mermaid as stmd
from oauth_secrets import main as load_oauth_secrets

if not os.path.exists('app/.streamlit/secrets.toml'):
    load_oauth_secrets()

st.set_page_config(
        page_title='Kaybee',
        page_icon='app/splash.png',
        layout='wide')
st.logo('app/bee.png', size='large', link=None)

# --- User and Session Management ---
if getattr(st.user, 'is_logged_in', False):
    st.session_state.user_id = st.user.sub
    company = 'Apple' # Assuming logged-in users are from Apple
    with st.sidebar:
        st.write(f"Hello, {st.user.name}!")
        if st.button("Log out"):
            st.logout()
else:
    st.session_state.user_id = 'default'
    company = 'Anonymous'
    with st.sidebar:
        if st.button("Log in with Google"):
            st.login('google')

if 'session_id' not in st.session_state:
    from agent_service import create_session
    st.session_state.session_id = create_session(
            st.session_state.user_id, company)

# --- Main Application UI ---
st.markdown('<h1 style="margin-top: 0rem; padding-top: 0rem">Tribal Knowledge Base</h1>', unsafe_allow_html=True)

AI_AVATAR = 'app/splash.png'
USER_AVATAR = '🧑'

if 'messages' not in st.session_state:
    st.session_state.messages = []

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
                with st.spinner("Thinking..."):
                    from agent_service import get_agent_response
                    agent_response = get_agent_response(
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            text=st.session_state.user_input.text,
                            files=st.session_state.user_input.files)
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
    with st.container():
        st.chat_input(
                'Teach me something...',
                key='user_input',
                accept_file=True,
                file_type=['pdf'])
with column2:
    with st.container():
        from agraph import get_agraph
        if agraph_clicked := get_agraph(graph_id=st.session_state.user_id):
            st.session_state.agraph_clicked = agraph_clicked
