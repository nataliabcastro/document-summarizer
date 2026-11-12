from pathlib import Path

def read_file(path: str) -> str:
    file = Path(path)
    suffix = file.suffix.lower()
    if suffix in (".txt", ".md"):
        return file.read_text(encoding="utf-8")
    if suffix == ".pdf":
        from pypdf import PdfReader
        pages = [page.extract_text() or "" for page in PdfReader(file).pages]
        return "\n".join(pages)
    if suffix == ".docx":
        from docx import Document
        return "\n".join(p.text for p in Document(file).paragraphs)
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup
        html = file.read_text(encoding="utf-8")
        return BeautifulSoup(html, "html.parser").get_text("\n")
    raise ValueError(f"File type not supported: {suffix}")