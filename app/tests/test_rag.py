class FakeDocument:
    """Mimics LangChain Document objects returned by the retriever."""
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


class FakeAIMessage:
    """Mimics ChatOllama AIMessage with a .content attribute."""
    def __init__(self, content):
        self.content = content


def test_retriever_simulated():
    """Simulates ContextualCompressionRetriever returning LangChain Documents."""

    def fake_retriever_invoke(query):
        return [
            FakeDocument(f"Info médicale pour: {query}", {"source": "Guide-des-Protocoles.md"}),
            FakeDocument("Rincer à l'eau de mer", {"source": "Guide-des-Protocoles.md"}),
        ]

    results = fake_retriever_invoke("piqûre de méduse")

    assert isinstance(results, list)
    assert len(results) == 2
    for doc in results:
        assert hasattr(doc, "page_content") and len(doc.page_content) > 0
        assert hasattr(doc, "metadata")


def test_llm_simulated():
    """Simulates ChatOllama (mistral-nemo) returning an AIMessage."""

    def fake_llm_invoke(prompt):
        return FakeAIMessage("Rincer à l'eau de mer et consulter un médecin.")

    response = fake_llm_invoke("Que faire en cas de piqûre de méduse ?")

    assert hasattr(response, "content")
    assert len(response.content) > 0


def test_pipeline_simulated():
    """Simulates the full RAG pipeline: retrieve → format → LLM → answer."""

    def fake_retriever_invoke(query):
        return [
            FakeDocument("Protocole piqûre de méduse: rincer à l'eau de mer."),
        ]

    def fake_llm_invoke(prompt):
        return FakeAIMessage("Il faut rincer à l'eau de mer.")

    question = "Que faire en cas de piqûre de méduse ?"
    docs = fake_retriever_invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    response = fake_llm_invoke(prompt)

    assert len(response.content) > 0
    assert isinstance(docs, list)
    assert len(docs) > 0