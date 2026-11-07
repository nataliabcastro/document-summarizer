# llm.py
import os

PROVIDER = os.getenv("PROVIDER", "local")
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "llama3.1")
CLOUD_BASE_URL = os.getenv("CLOUD_BASE_URL", "")  # an OpenAI-compatible API with a free plan
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY", "")
CLOUD_MODEL = os.getenv("CLOUD_MODEL", "")
ANTHROPIC_MODEL = "claude-sonnet-5-5"

def call_model(system: str, user: str) -> str:
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]

    if PROVIDER == "local":
        from ollama import chat
        response = chat(model=LOCAL_MODEL, messages=messages, options={"temperature": 0.2})
        return response.message.content

    if PROVIDER == "cloud":
        from openai import OpenAI
        client = OpenAI(base_url=CLOUD_BASE_URL, api_key=CLOUD_API_KEY)
        response = client.chat.completions.create(
            model=CLOUD_MODEL, messages=messages, temperature=0.2, max_tokens=1500)
        return response.choices[0].message.content

    if PROVIDER != "anthropic":
        raise ValueError(f"PROVIDER inválido: {PROVIDER!r}. Use local, cloud ou anthropic.")
    from anthropic import Anthropic
    message = Anthropic().messages.create(
        model=ANTHROPIC_MODEL, max_tokens=1500, system=system,
        messages=[{"role": "user", "content": user}])
    return message.content[0].text

if __name__ == "__main__":
    print(call_model("Responda em uma frase.", "O que é um resumo?"))