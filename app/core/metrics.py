"""
Prometheus metrics for the CliniQ RAG application.
Exposes: request counts, latency histograms, error counters, quality gauges.
"""
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
)

# ── Request counters ──────────────────────────────────────────
rag_pipeline_calls_total = Counter(
    "rag_pipeline_calls_total",
    "Total number of RAG pipeline calls",
)

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests to the API",
    ["method", "endpoint", "status_code"],
)

# ── Latency histograms ───────────────────────────────────────
rag_latency_seconds = Histogram(
    "rag_latency_seconds",
    "End-to-end RAG pipeline latency in seconds",
    buckets=[0.5, 1, 2, 5, 10, 20, 30, 60],
)

rag_retrieval_latency_seconds = Histogram(
    "rag_retrieval_latency_seconds",
    "Retriever latency in seconds",
    buckets=[0.1, 0.25, 0.5, 1, 2, 5, 10],
)

rag_llm_latency_seconds = Histogram(
    "rag_llm_latency_seconds",
    "LLM inference latency in seconds",
    buckets=[0.5, 1, 2, 5, 10, 20, 30],
)

# ── Error counters ────────────────────────────────────────────
rag_errors_total = Counter(
    "rag_errors_total",
    "Total RAG pipeline errors",
    ["error_type"],
)

# ── Quality gauges ────────────────────────────────────────────
rag_answer_relevance = Gauge(
    "rag_answer_relevance",
    "Answer relevance score (0-1)",
)

rag_faithfulness = Gauge(
    "rag_faithfulness",
    "Answer faithfulness score (0-1)",
)

rag_retrieved_docs = Gauge(
    "rag_retrieved_docs",
    "Number of documents returned by the last retrieval",
)

rag_answer_length = Gauge(
    "rag_answer_length",
    "Character length of the last RAG answer",
)
