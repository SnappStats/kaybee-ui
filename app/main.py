import logging
import json
import os
import streamlit as st
import streamlit_mermaid as stmd
from stt import transcribe_audio

from oauth_secrets import main as load_oauth_secrets
from agent_service import stream_agent_response, create_session
from agraph import get_agraph
from knowledge_graph_service import fetch_entity

AI_AVATAR = 'app/splash.png'
USER_AVATAR = '🧑'

def handle_chat_input():
    if text := st.session_state.chat_input.text:
        st.session_state.user_input = {
                'text': text,
                'files': st.session_state.chat_input.files
        }

def handle_audio_input():
    if text := transcribe_audio(st.session_state.audio_input.getvalue()):
        st.session_state.user_input = {'text': text, 'files': []}

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
    st.session_state.user_id = 'anonymous'
    company = 'AYSO'
    with st.sidebar:
        if st.button("Log in with Google"):
            st.login('google')

if 'session_id' not in st.session_state:
    try:
        st.session_state.session_id = create_session(
                st.session_state.user_id, company)
    except Exception as e:
        logging.error(f"Error creating session: {e}")
        st.write('Broken, sorry.')
        st.stop()

if 'agraph_clicked' not in st.session_state:
    st.session_state.agraph_clicked = None

# --- Main Application UI ---
st.markdown('<h1 style="margin-top: 0rem; padding-top: 0rem">Tribal Knowledge Base</h1>', unsafe_allow_html=True)

def format_response(snippet: dict):
    for item in snippet:
        if item.get('partial'):
            continue
        if not (parts := item.get('content', {}).get('parts', [])):
            continue
        for part in parts:
            if text := part.get('text'):
                if part.get('thought'):
                    if author := item.get('author'):
                        st.caption(f"[{author}]")
                    st.caption(text)
                else:
                    try:
                        json.loads(text)
                    except:
                        if author := item.get('author'):
                            st.write(f"[{author}]")
                        st.markdown(text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": text})

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.container(border=False):
    colAI, colGraph, colDetails = st.columns([1,2,1], border=True)
    with colAI:
        with st.container(height=500, border=False):
            for message in st.session_state.messages:
                if message['role'] == 'user':
                    with st.chat_message("user", avatar=USER_AVATAR):
                        st.markdown(message['content'])
                else:
                    with st.chat_message("assistant", avatar=AI_AVATAR):
                        st.markdown(message['content'])

            if user_input := st.session_state.get('user_input'):
                with st.chat_message("user", avatar=USER_AVATAR):
                    st.markdown(user_input['text'])
                    st.session_state.messages.append(
                        {"role": "user", "content": user_input['text']})
                with st.chat_message("assistant", avatar=AI_AVATAR):
                    with st.spinner("Thinking..."):
                        try:
                            agent_response = stream_agent_response(
                                    user_id=st.session_state.user_id,
                                    session_id=st.session_state.session_id,
                                    text=user_input['text'],
                                    files=user_input['files'])
                        except Exception as e:
                            logging.error(f"Error in agent response: {e}")
                            st.error("Sorry, the session is stale.")
                            st.stop()
                        format_response(agent_response)
                st.session_state['user_input'] = None

        with st.container():
            if st.toggle('🎤', value=False):
                st.audio_input(
                    'voice',
                    label_visibility='collapsed',
                    on_change=handle_audio_input,
                    key='audio_input')
            else:
                st.chat_input(
                    'Teach me something...',
                    key='chat_input',
                    accept_file=True,
                    file_type=['pdf'],
                    on_submit=handle_chat_input)
    with colGraph:
        with st.container():
            if agraph_clicked := get_agraph(graph_id=st.session_state.user_id):
                st.session_state.agraph_clicked = agraph_clicked

    with colDetails:
        if st.session_state.agraph_clicked:
            entity = fetch_entity(
                    graph_id=st.session_state.user_id,
                    entity_id=st.session_state.agraph_clicked)
            st.subheader(entity['entity_names'][0])
            st.json(entity)
