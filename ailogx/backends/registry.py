# ailogx/backends/registry.py

import os

def get_analyzer():
    backend = os.environ.get("LLM_LOGGER_BACKEND", "ollama").lower()

    if backend == "groq":
        from ailogx.backends import groq
        return groq.Model()

    elif backend == "openai":
        from ailogx.backends import openai
        return openai.Model()

    elif backend == "ollama":
        from ailogx.backends import ollama
        return ollama.Model()

    elif backend == "anthropic" or backend == "claude":
        from ailogx.backends import anthropic
        return anthropic.Model()

    elif backend == "xai" or backend == "grok":
        from ailogx.backends import xai
        return xai.Model()

    else:
        raise ValueError(f"Unsupported LLM backend: {backend}")