import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

from backend.services.knowledge_loader import (
    load_knowledge_documents
)

# -----------------------------------
# GLOBAL CACHE
# -----------------------------------

embedding_model = None

documents = None

index = None


# -----------------------------------
# INITIALIZE RAG
# -----------------------------------

def initialize_rag():

    global embedding_model
    global documents
    global index

    # Prevent reloading repeatedly
    if index is not None:

        return

    print("Initializing FTIO RAG Engine...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    documents = load_knowledge_documents()

    document_texts = [

        doc["content"]

        for doc in documents
    ]

    embeddings = embedding_model.encode(
        document_texts
    )

    embedding_matrix = np.array(
        embeddings
    ).astype("float32")

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
# RETRIEVE CONTEXT
# -----------------------------------

def retrieve_context(
    query,
    top_k=2
):

    # Lazy initialize
    initialize_rag()

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