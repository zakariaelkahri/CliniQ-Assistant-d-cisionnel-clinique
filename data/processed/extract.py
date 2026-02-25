from llama_parse import LlamaParse
from app.core.config import settings


pdf_path = "../raw/Guide-des-Protocoles.pdf"
md_output = "./Guide-des-Protocoles.md"

parser = LlamaParse(
    api_key=settings.LLAMA_KEY,
    result_type="markdown",
    language="fr",
    verbose=True,
    premium_mode=True,
    disable_ocr=True,   
)

documents = parser.load_data(pdf_path)

with open(md_output, "w", encoding="utf-8") as f:
    for doc in documents:
        f.write(doc.text)
        f.write("\n\n---\n\n")

print(f"Markdown saved to {md_output}")