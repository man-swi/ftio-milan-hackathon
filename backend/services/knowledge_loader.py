from pathlib import Path


KNOWLEDGE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    / "knowledge"
)


def load_knowledge_documents():

    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*.md"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

            documents.append({

                "source": str(file_path),

                "content": content
            })

    return documents