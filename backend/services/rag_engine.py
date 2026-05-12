import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from backend.services.knowledge_loader import (
    load_knowledge_documents
)


# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# LOAD KNOWLEDGE DOCS
# -----------------------------------

documents = load_knowledge_documents()

document_texts = [

    doc["content"]

    for doc in documents
]

# -----------------------------------
# CREATE EMBEDDINGS
# -----------------------------------

embeddings = embedding_model.encode(
    document_texts
)

embedding_matrix = np.array(
    embeddings
).astype("float32")

# -----------------------------------
# BUILD FAISS INDEX
# -----------------------------------

dimension = embedding_matrix.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(embedding_matrix)

print(
    f"FTIO RAG loaded "
    f"{len(documents)} documents."
)

# -----------------------------------
# RETRIEVAL FUNCTION
# -----------------------------------

def retrieve_context(
    query,
    top_k=2
):

    query_embedding = (
        embedding_model.encode([query])
    )

    query_vector = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_vector,
        top_k
    )

    retrieved_docs = []

    for idx in indices[0]:

        retrieved_docs.append(

            documents[idx]["content"]
        )

    return "\n\n".join(
        retrieved_docs
    )