from backend.services.rag_engine import (
    retrieve_context
)

query = (
    "luxury fashion pricing strategy"
)

results = retrieve_context(query)

print("\n")
print("RETRIEVED KNOWLEDGE:")
print("\n")
print(results)