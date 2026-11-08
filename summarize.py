import sys
from pathlib import Path
from langdetect import detect, DetectorFactory
from llm import call_model

DetectorFactory.seed = 0   # makes the detection give the same answer every time

LANGUAGES = {"pt": "Brazilian Portuguese", "en": "English", "es": "Spanish",
             "fr": "French", "de": "German", "it": "Italian"}
SAME_LANGUAGE = "the same language as the text"

def detect_language(text: str) -> str:
    try:
        return LANGUAGES.get(detect(text[:3000]), SAME_LANGUAGE)
    except Exception:          # empty text, only numbers, etc.
        return SAME_LANGUAGE

def summarize_text(text: str, target: str = "6 to 10 bullet points") -> str:
    system = Path("prompts/summarize_v1.md").read_text(encoding="utf-8")
    user = f'Language: {detect_language(text)}\nLength: {target}\n\nText:\n"""{text}"""'
    return call_model(system, user)

if __name__ == "__main__":
    print(summarize_text(Path(sys.argv[1]).read_text(encoding="utf-8")))