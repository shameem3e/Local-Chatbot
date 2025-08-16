import requests
import streamlit as st
from config.frontend_config import frontend_settings

# ---- Basic page setup ----
st.set_page_config(page_title="ChatBot", page_icon="💬", layout="centered")
st.title("🤖 AI ChatBot")

# ---- Backend URL from config ----
API_HOST = frontend_settings.API_HOST
API_PORT = frontend_settings.API_PORT
PROVIDER_MODELS_URL = f"http://{API_HOST}:{API_PORT}/api/provider-models"
CHAT_URL = f"http://{API_HOST}:{API_PORT}/api/chat"

# ---- Providers and models ----
PROVIDER_MODELS = requests.get(PROVIDER_MODELS_URL).json()

# ---- Conversation API URLs ----
CONVERSATIONS_URL = f"http://{API_HOST}:{API_PORT}/api/conversations"
CONVERSATION_URL = f"http://{API_HOST}:{API_PORT}/api/conversation"
TITLE_URL = f"http://{API_HOST}:{API_PORT}/api/title"
ADD_MESSAGE_URL = f"http://{API_HOST}:{API_PORT}/api/add_message"

# ---- Session defaults ----
st.session_state.setdefault("provider", list(PROVIDER_MODELS.keys())[0])
st.session_state.setdefault("model", PROVIDER_MODELS[list(PROVIDER_MODELS.keys())[0]][0])
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("show_settings", False)
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)

# ---- Settings toggle ----
_, settings_col = st.columns([10, 1])
with settings_col:
    if st.button("⚙️", help="Model settings"):
        st.session_state.show_settings = not st.session_state.show_settings

# ---- Model settings ----
if st.session_state.show_settings:
    with st.expander("🛠️ Model Settings", expanded=True):
        providers_list = list(PROVIDER_MODELS.keys())
        provider = st.selectbox("Provider", providers_list, index=providers_list.index(st.session_state.provider))
        model = st.selectbox("Model", PROVIDER_MODELS[provider],
                             index=PROVIDER_MODELS[provider].index(
                                 st.session_state.model if st.session_state.model in PROVIDER_MODELS[provider]
                                 else PROVIDER_MODELS[provider][0]
                             ))
        st.session_state.provider, st.session_state.model = provider, model
        st.success(f"Using {provider} • {model}")

# ---- Sidebar: Conversations ----
with st.sidebar:
    st.header("💬 History")
    # Fetch all conversations
    try:
        conversations = requests.get(CONVERSATIONS_URL).json()
    except Exception:
        conversations = {}
    # New Chat button
    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.chat_history = []
        st.session_state.conversation_title = None
    # List conversations
    for cid, title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        button_label = f"**{title}**" if is_current else title
        if st.button(button_label, key=cid):
            # Load conversation
            conv = requests.get(f"{CONVERSATION_URL}/{cid}").json()
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = conv.get("title", "Untitled")
            st.session_state.chat_history = conv.get("messages", [])

# ---- Show chat so far ----
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
user_text = st.chat_input("Ask AI...")
if user_text:
    # show + store user message
    st.chat_message("user").markdown(user_text)
    st.session_state.chat_history.append({"role": "user", "content": user_text})

    if st.session_state.conversation_id is None:
        # New conversation: generate title, create conversation
        title_payload = {
            "provider": st.session_state.provider,
            "model": st.session_state.model,
            "query": user_text,
        }
        try:
            title_resp = requests.post(TITLE_URL, json=title_payload)
            title = title_resp.json().get("title", "New Chat")
        except Exception:
            title = "New Chat"
        conv_payload = {
            "title": title,
            "role": "user",
            "content": user_text,
        }
        conv_resp = requests.post(CONVERSATION_URL, json=conv_payload)
        conv_data = conv_resp.json()
        st.session_state.conversation_id = conv_data.get("conversation_id")
        st.session_state.conversation_title = conv_data.get("title", title)
        st.session_state.chat_history = [conv_data.get("first_message")]
    else:
        # Existing conversation: add message
        add_msg_payload = {
            "conversation_id": st.session_state.conversation_id,
            "role": "user",
            "content": user_text,
        }
        requests.post(ADD_MESSAGE_URL, json=add_msg_payload)

    # get assistant reply
    payload = {
        "provider": st.session_state.provider,
        "model": st.session_state.model,
        "chat_history": [{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history],
    }
    response = requests.post(CHAT_URL, json=payload)
    assistant_response = response.json().get("response", "[No response from assistant]")

    # show + store assistant message
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Add assistant message to conversation if exists
    if st.session_state.conversation_id:
        add_msg_payload = {
            "conversation_id": st.session_state.conversation_id,
            "role": "assistant",
            "content": assistant_response,
        }
        requests.post(ADD_MESSAGE_URL, json=add_msg_payload)
