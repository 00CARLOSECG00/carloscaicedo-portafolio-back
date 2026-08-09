"""Static knowledge graph — mirrors `carloscaicedo-portfolio/data/fallback/knowledge.ts`."""

from app.models.schemas import GraphEdge, KnowledgeGraphResponse, KnowledgeNode

KNOWLEDGE_NODES: list[KnowledgeNode] = [
    KnowledgeNode(
        id="ai",
        label="Artificial Intelligence",
        group="core",
        description="Systems that reason, learn and act on data to solve problems that once needed a human.",
        related=["ml", "nlp", "llms", "ai-apps"],
        projects=["talk-to-my-ai"],
    ),
    KnowledgeNode(
        id="ml",
        label="Machine Learning",
        group="ai",
        description="Learning patterns from data instead of hand-writing rules — the engine behind most modern AI.",
        related=["ai", "embeddings", "vector-db"],
        technologies=["scikit-learn", "PyTorch"],
    ),
    KnowledgeNode(
        id="nlp",
        label="NLP",
        group="ai",
        description="Teaching machines to read, understand and generate human language.",
        related=["ai", "llms", "embeddings"],
        projects=["nlp-playground"],
    ),
    KnowledgeNode(
        id="llms",
        label="LLMs",
        group="ai",
        description="Large language models that generate and reason over text, powering assistants and RAG.",
        related=["nlp", "rag", "ai"],
        projects=["talk-to-my-ai"],
    ),
    KnowledgeNode(
        id="rag",
        label="RAG",
        group="ai",
        description=(
            "Retrieval-Augmented Generation connects language models with external knowledge sources "
            "so answers stay grounded and current."
        ),
        related=["embeddings", "vector-db", "llms"],
        projects=["talk-to-my-ai"],
    ),
    KnowledgeNode(
        id="embeddings",
        label="Embeddings",
        group="data",
        description="Numeric representations of meaning that let machines compare text, images and records by similarity.",
        related=["rag", "vector-db", "nlp"],
    ),
    KnowledgeNode(
        id="retrieval",
        label="Retrieval",
        group="data",
        description="Finding the most relevant pieces of knowledge for a query before generation happens.",
        related=["rag", "vector-db"],
    ),
    KnowledgeNode(
        id="ai-apps",
        label="AI Applications",
        group="ai",
        description="Turning models into real products — assistants, search, analytics and automation.",
        related=["ai", "llms"],
        projects=["talk-to-my-ai", "nlp-playground"],
    ),
    KnowledgeNode(
        id="databases",
        label="Databases",
        group="core",
        description="The many ways data can be stored and queried — each shaped by the questions you need to answer.",
        related=["relational", "document", "columnar", "key-value", "vector-db", "graph", "geospatial"],
        projects=["database-lab"],
    ),
    KnowledgeNode(
        id="relational",
        label="Relational",
        group="db",
        description="Tables, rows and joins — the reliable default for structured, related data.",
        related=["databases"],
    ),
    KnowledgeNode(
        id="document",
        label="Document",
        group="db",
        description="Flexible JSON-like documents that keep related data together.",
        related=["databases"],
    ),
    KnowledgeNode(
        id="columnar",
        label="Columnar",
        group="db",
        description="Column-oriented storage built for fast analytics over huge datasets.",
        related=["databases"],
    ),
    KnowledgeNode(
        id="key-value",
        label="Key-Value",
        group="db",
        description="Blazing-fast lookups by key — ideal for caching and sessions.",
        related=["databases"],
    ),
    KnowledgeNode(
        id="vector-db",
        label="Vector Databases",
        group="db",
        description="Store embeddings and search by meaning rather than exact matches — the backbone of RAG.",
        related=["databases", "embeddings", "rag"],
        projects=["database-lab"],
    ),
    KnowledgeNode(
        id="graph",
        label="Graph",
        group="db",
        description="Nodes and relationships that make connected data a first-class citizen.",
        related=["databases"],
    ),
    KnowledgeNode(
        id="geospatial",
        label="Geospatial",
        group="db",
        description="Data anchored to places, queried by distance, region and shape.",
        related=["databases"],
    ),
]


def _build_edges() -> list[GraphEdge]:
    edges: list[GraphEdge] = []
    seen: set[str] = set()
    for node in KNOWLEDGE_NODES:
        for target in node.related:
            key = "::".join(sorted([node.id, target]))
            if key in seen:
                continue
            seen.add(key)
            edges.append(GraphEdge(source=node.id, target=target))
    return edges


def static_knowledge_graph() -> KnowledgeGraphResponse:
    return KnowledgeGraphResponse(nodes=KNOWLEDGE_NODES, edges=_build_edges())


def knowledge_node_by_id(node_id: str) -> KnowledgeNode | None:
    return next((n for n in KNOWLEDGE_NODES if n.id == node_id), None)
