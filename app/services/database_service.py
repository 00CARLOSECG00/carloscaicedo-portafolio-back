"""Database Lab views derived from the single fictional dataset."""

from __future__ import annotations

import math

from app.data.dataset import CUSTOMERS, ORDERS, PRODUCTS, REVIEWS, customer_by_id, product_by_id
from app.models.schemas import (
    ColumnarColumn,
    ColumnarResponse,
    DocumentResponse,
    GeoFeature,
    GeospatialResponse,
    GraphEdge,
    GraphNode,
    GraphResponse,
    KeyValueEntry,
    KeyValueResponse,
    RelationalResponse,
    RelationalTable,
    VectorRecord,
    VectorSearchResponse,
)

VECTOR_TERMS = [
    "technology",
    "gaming",
    "photography",
    "audio",
    "data",
    "design",
    "music",
    "travel",
    "cloud",
    "productivity",
    "hardware",
    "streaming",
]


def _embed(tokens: list[str]) -> list[float]:
    return [1.0 if any(t in term or term in t for t in tokens) else 0.0 for term in VECTOR_TERMS]


def _tokenize_interests(interests: list[str]) -> list[str]:
    return [i.lower() for i in interests]


def _project(vec: list[float], seed: int) -> tuple[float, float]:
    x = 0.0
    y = 0.0
    for i, v in enumerate(vec):
        x += v * math.cos((i + seed) * 1.7)
        y += v * math.sin((i + seed) * 1.3)
    return x, y


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def get_relational() -> RelationalResponse:
    return RelationalResponse(
        tables=[
            RelationalTable(
                name="customers",
                columns=["id", "name", "city", "country", "segment"],
                rows=[[c.id, c.name, c.city, c.country, c.segment] for c in CUSTOMERS],
            ),
            RelationalTable(
                name="products",
                columns=["id", "name", "category", "price"],
                rows=[[p.id, p.name, p.category, f"${p.price}"] for p in PRODUCTS],
            ),
            RelationalTable(
                name="orders",
                columns=["id", "customer", "product", "qty", "date"],
                rows=[
                    [
                        o.id,
                        customer_by_id(o.customer_id).name if customer_by_id(o.customer_id) else str(o.customer_id),
                        product_by_id(o.product_id).name if product_by_id(o.product_id) else str(o.product_id),
                        o.quantity,
                        o.date,
                    ]
                    for o in ORDERS
                ],
            ),
        ]
    )


def get_document() -> DocumentResponse:
    documents = []
    for c in CUSTOMERS[:4]:
        documents.append(
            {
                "_id": f"cust_{c.id}",
                "name": c.name,
                "location": {"city": c.city, "country": c.country},
                "segment": c.segment,
                "interests": c.interests,
                "orders": [
                    {
                        "product": product_by_id(o.product_id).name if product_by_id(o.product_id) else None,
                        "quantity": o.quantity,
                        "date": o.date,
                    }
                    for o in ORDERS
                    if o.customer_id == c.id
                ],
            }
        )
    return DocumentResponse(collection="customers", documents=documents)


def get_columnar() -> ColumnarResponse:
    return ColumnarResponse(
        table="orders",
        columns=[
            ColumnarColumn(
                name="product",
                type="string",
                values=[product_by_id(o.product_id).name if product_by_id(o.product_id) else "" for o in ORDERS],
                note="Grouped and scanned independently of other columns.",
            ),
            ColumnarColumn(
                name="quantity",
                type="int",
                values=[o.quantity for o in ORDERS],
                note="Compresses well — ideal for SUM / AVG aggregations.",
            ),
            ColumnarColumn(
                name="date",
                type="date",
                values=[o.date for o in ORDERS],
                note="Enables fast time-range analytics without touching other fields.",
            ),
        ],
    )


def get_key_value() -> KeyValueResponse:
    return KeyValueResponse(
        entries=[
            KeyValueEntry(
                key=f"customer:{c.id}",
                value={"name": c.name, "city": c.city, "segment": c.segment, "interests": c.interests},
            )
            for c in CUSTOMERS
        ]
    )


def search_vectors(query: str, top_k: int = 5) -> VectorSearchResponse:
    q_tokens = [t for t in query.lower().split() if t]
    q_vec = _embed(q_tokens)

    records: list[VectorRecord] = []
    for c in CUSTOMERS:
        c_vec = _embed(_tokenize_interests(c.interests))
        x, y = _project(c_vec, c.id)
        score = _cosine(q_vec, c_vec)
        records.append(
            VectorRecord(
                id=f"cust_{c.id}",
                label=c.name,
                description=f"{c.segment} in {c.city} · {', '.join(c.interests)}",
                x=x,
                y=y,
                score=score,
            )
        )

    records.sort(key=lambda r: r.score or 0, reverse=True)
    return VectorSearchResponse(query=query, records=records[:top_k])


def get_graph() -> GraphResponse:
    nodes: list[GraphNode] = [
        *[GraphNode(id=f"c{c.id}", label=c.name, group="customer") for c in CUSTOMERS[:5]],
        *[GraphNode(id=f"p{p.id}", label=p.name, group="product") for p in PRODUCTS],
        *[
            GraphNode(id=f"city_{city}", label=city, group="location")
            for city in sorted({c.city for c in CUSTOMERS[:5]})
        ],
    ]
    edges: list[GraphEdge] = [
        *[GraphEdge(source=f"c{o.customer_id}", target=f"p{o.product_id}", label="bought") for o in ORDERS if o.customer_id <= 5],
        *[GraphEdge(source=f"c{c.id}", target=f"city_{c.city}", label="lives in") for c in CUSTOMERS[:5]],
        *[
            GraphEdge(source=f"c{r.customer_id}", target=f"p{r.product_id}", label="reviewed")
            for r in REVIEWS
            if r.customer_id <= 5
        ],
    ]
    return GraphResponse(nodes=nodes, edges=edges)


def get_geospatial() -> GeospatialResponse:
    return GeospatialResponse(
        features=[
            GeoFeature(
                id=f"cust_{c.id}",
                label=f"{c.name} — {c.city}",
                latitude=c.latitude,
                longitude=c.longitude,
                value=len([o for o in ORDERS if o.customer_id == c.id]),
                category=c.segment,
            )
            for c in CUSTOMERS
        ]
    )
