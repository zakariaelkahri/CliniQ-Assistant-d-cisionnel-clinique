from app.rag.embeddings import documents, embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


client = QdrantClient(url="http://qdrant:6333")

try:
    client.delete_collection(collection_name="medical_manual")
    print("Deleted existing collection")
except Exception as e:
    print(f"No collection to delete: {e}")

vectorstore = QdrantVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    url="http://qdrant:6333",
    collection_name="medical_manual"
)
