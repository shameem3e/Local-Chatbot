import uuid
from datetime import datetime, UTC

from backend.db.chat_dao import chat_store, Q

conversations = chat_store.conversations

def add_message(conv_id: str, role: str, content: str):
    cond = Q[conv_id].exists()
    doc = conversations.get(cond)
    new_msg = {"role": role, "content": content}

    if doc is not None:
        # Append new message without touching the title
        data = doc[conv_id]
        data["messages"] = data["messages"] + [new_msg]
        data["last_interacted"] = datetime.now(UTC).isoformat()
        conversations.update({conv_id: data}, cond)

def get_conversation(conv_id: str):
    doc = conversations.get(Q[conv_id].exists())
    if doc:
        # Update last_interacted on access
        data = doc[conv_id]
        data["last_interacted"] = datetime.now(UTC).isoformat()
        conversations.update({conv_id: data}, Q[conv_id].exists())
        return data
    return None

def get_all_conversations():
    """Returns a dict of conv_id: title for all conversations, with most recent first."""
    all_convs = [conv for conv in conversations.all()]
    convs_with_time = []
    for conv in all_convs:
        conv_id = list(conv.keys())[0]
        data = list(conv.values())[0]
        last = data.get("last_interacted", "1970-01-01T00:00:00")
        convs_with_time.append((conv_id, data["title"], last))
    convs_with_time.sort(key=lambda x: x[2], reverse=True)
    return {cid: title for cid, title, _ in convs_with_time}

def create_new_conversation_id():
    """Generate a new UUID for conversation ID."""
    return str(uuid.uuid4())

def create_new_conversation(title: str = None, role: str = None, content: str = None) -> str:
    """Create a new conversation with an optional title and the first message. Returns the new conversation ID."""
    conv_id = create_new_conversation_id()
    messages = []
    if role and content:
        messages.append({"role": role, "content": content})
    conversations.insert({
        conv_id: {
            "title": title or "Untitled Conversation",
            "messages": messages,
            "last_interacted": datetime.now(UTC).isoformat()
        }
    })
    return conv_id

# --- Example usage ---

# For a new conversation (with the first message):
# conv_id = create_new_conversation(title="Intro to Deep Learning", role="user", content="What is DL?")
# add_message(conv_id, "assistant", "Answer for DL query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # For an existing conversation:
# add_message(conv_id, "user", "What is ML?")
# add_message(conv_id, "assistant", "Answer for ML query")
# print(get_conversation(conv_id))
# print(get_all_conversations())
#
# # For a new conversation (with a different title and first message):
# conv_id2 = create_new_conversation(title="Intro to Generative AI", role="user", content="What is Generative AI?")
# add_message(conv_id2, "assistant", "Answer for Generative AI query")
# print(get_conversation(conv_id2))
# print(get_all_conversations())
