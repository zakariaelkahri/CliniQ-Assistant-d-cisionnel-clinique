from app.rag.embeddings import embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

client = QdrantClient(url="http://qdrant:6333")

vectorstore = QdrantVectorStore(
    client=client,
    collection_name="medical_manual",
    embedding=embeddings
)

base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

compressor = CrossEncoderReranker(model=model, top_n=5)

retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# query = "Quel est le principal risque associé à la gastro-entérite pédiatrique ?"
# results = retriever.invoke(query)

# for r in results:
#     print( r.page_content)
#     # print(f"Metadata: {r.metadata}")
#     print("-" * 50)