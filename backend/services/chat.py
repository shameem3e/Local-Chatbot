from llama_index.core.llms import ChatMessage

from backend.llm.llm_factory import get_llm


def chat_qa(provider: str, model: str, chat_history: list) -> str:
    """Perform a chat-based Q&A using the specified LLM provider and model."""
    llm = get_llm(provider, model)
    messages = [ChatMessage(role=m["role"], content=m["content"]) for m in chat_history]
    response = llm.chat(messages)
    return response.message.content


# Example usage of the chat_qa function
# provider = "ollama"
# model = "gemma:2b"
# chat_history = [
#     {"role": "system", "content": "You are a helpful assistant"},
#     {"role": "user", "content": "What is Deep Learning?"}
# ]
# response = chat_qa(provider, model, chat_history)
# print(response)
