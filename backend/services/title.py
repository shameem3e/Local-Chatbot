from backend.llm.llm_factory import get_llm
import json

def get_chat_title(provider: str, model: str, query: str) -> dict:
    llm = get_llm(provider, model)
    prompt = (
        "Generate a very short and concise title (max 5 words) for the following user query. "
        "Respond ONLY with a JSON object in the format: {\"title\": \"<your generated title>\"}. "
        "User query: " + query
    )
    response = llm.complete(prompt=prompt)
    response_text = response.text if hasattr(response, 'text') else str(response)
    return json.loads(response_text)


# example usage
# title = title_generation("ollama", "mistral:7b", "What is Machine Learning?")
# print(title)
