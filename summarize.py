import sys
from pathlib import Path
from llm import call_model

def summarize_text(text: str, target: str = "6 to 10 bullet points") -> str:
    system = Path("prompts/summarize_v1.md").read_text(encoding="utf-8")
    user = f'Length: {target}\n\nText:\n"""{text}"""'
    return call_model(system, user)

if __name__ == "__main__":
    print(summarize_text(Path(sys.argv[1]).read_text(encoding="utf-8")))