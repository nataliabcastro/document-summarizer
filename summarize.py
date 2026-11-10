import sys
from pathlib import Path
from langdetect import detect, DetectorFactory
from checker import missing_numbers
from llm import call_model

DetectorFactory.seed = 0   # makes the detection give the same answer every time

LANGUAGES = {"pt": "Brazilian Portuguese", "en": "English", "es": "Spanish",
             "fr": "French", "de": "German", "it": "Italian"}
SAME_LANGUAGE = "the same language as the text"

MESSAGES = {
    "Brazilian Portuguese": {
        "warning": "ATENÇÃO: estes números estão no resumo, mas não aparecem no texto original: ",
        "check": "Confira à mão antes de usar o resumo.",
        "ok": "Conferência de números: todos os números do resumo aparecem no texto original."},
    "English": {
        "warning": "WARNING: these numbers are in the summary but do not appear in the original text: ",
        "check": "Check them by hand before using the summary.",
        "ok": "Number check: all numbers in the summary appear in the original text."},
    "Spanish": {
        "warning": "ATENCIÓN: estos números están en el resumen, pero no aparecen en el texto original: ",
        "check": "Compruébalos a mano antes de usar el resumen.",
        "ok": "Comprobación de números: todos los números del resumen aparecen en el texto original."},
    "French": {
        "warning": "ATTENTION : ces nombres figurent dans le résumé mais pas dans le texte original : ",
        "check": "Vérifiez-les à la main avant d'utiliser le résumé.",
        "ok": "Vérification des nombres : tous les nombres du résumé figurent dans le texte original."},
    "German": {
        "warning": "ACHTUNG: Diese Zahlen stehen in der Zusammenfassung, kommen im Originaltext aber nicht vor: ",
        "check": "Bitte prüfe sie von Hand, bevor du die Zusammenfassung verwendest.",
        "ok": "Zahlenprüfung: Alle Zahlen der Zusammenfassung kommen im Originaltext vor."},
    "Italian": {
        "warning": "ATTENZIONE: questi numeri sono nel riassunto ma non compaiono nel testo originale: ",
        "check": "Controllali a mano prima di usare il riassunto.",
        "ok": "Controllo dei numeri: tutti i numeri del riassunto compaiono nel testo originale."},
}

def detect_language(text: str) -> str:
    try:
        return LANGUAGES.get(detect(text[:3000]), SAME_LANGUAGE)
    except Exception:          # empty text, only numbers, etc.
        return SAME_LANGUAGE

def keep_bullets(summary: str) -> str:
    lines = [l for l in summary.splitlines() if l.strip().startswith(("- ", "* ", "• "))]
    return "\n".join(lines) if lines else summary

def summarize_text(text: str, target: str = "6 to 10 bullet points") -> str:
    system = Path("prompts/summarize_v1.md").read_text(encoding="utf-8")
    user = f'Language: {detect_language(text)}\nLength: {target}\n\nText:\n"""{text}"""'
    return keep_bullets(call_model(system, user))

if __name__ == "__main__":
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    summary = summarize_text(text)
    print(summary)
    messages = MESSAGES.get(detect_language(text), MESSAGES["English"])
    missing = missing_numbers(text, summary)
    if missing:
        print("\n" + messages["warning"] + ", ".join(missing))
        print(messages["check"])
    else:
        print("\n" + messages["ok"])