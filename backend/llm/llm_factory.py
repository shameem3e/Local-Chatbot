# llm_factory: A simple factory to create and cache LLM instances

from llama_index.llms.ollama import Ollama
from llama_index.llms.groq import Groq
from llama_index.llms.openai import OpenAI

# Map provider name -> class
LLM_BY_PROVIDER = {
    "ollama": Ollama,
    "groq": Groq,
    "openai": OpenAI,
}

# Single-slot cache
_current_key = None      # tuple: (provider, model)
_current_llm = None      # the cached LLM instance


def get_llm(provider: str, model: str):
    """Return the (provider, model) LLM instance.
    Only one instance is kept in memory at a time.
    """
    global _current_key, _current_llm
    key = (provider, model)

    # If it's already the current one, reuse it
    if _current_key == key and _current_llm is not None:
        return _current_llm

    # Build a new instance and replace the cache
    if provider not in LLM_BY_PROVIDER:
        raise ValueError(f"Unsupported provider: {provider}")

    _current_llm = LLM_BY_PROVIDER[provider](model=model)
    _current_key = key
    return _current_llm


def reset_llm_cache():
    """Clear the single-slot cache (optional helper)."""
    global _current_key, _current_llm
    _current_key = None
    _current_llm = None


# --- Example (for your video narration) ---
# llm = get_llm("ollama", "llama3:8b")
# llm2 = get_llm("ollama", "llama3:70b")  # replaces the previous instance
# same_llm2 = get_llm("ollama", "llama3:70b")  # returns the cached one
