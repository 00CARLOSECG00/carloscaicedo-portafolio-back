"""Knowledge graph service — Supabase when configured, static data otherwise."""

from __future__ import annotations

import logging

from app.config import Settings, get_settings
from app.data.knowledge import knowledge_node_by_id, static_knowledge_graph
from app.models.schemas import GraphEdge, KnowledgeGraphResponse, KnowledgeNode
from app.services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


def get_knowledge_graph(settings: Settings | None = None) -> KnowledgeGraphResponse:
    settings = settings or get_settings()
    if settings.use_supabase_knowledge and settings.supabase_enabled:
        client = get_supabase_client(settings)
        if client:
            try:
                nodes_resp = (
                    client.table("knowledge_nodes")
                    .select("*")
                    .eq("is_active", True)
                    .order("sort_order")
                    .execute()
                )
                edges_resp = client.table("knowledge_edges").select("*").execute()
                if nodes_resp.data:
                    nodes = [
                        KnowledgeNode(
                            id=row["id"],
                            label=row["label"],
                            group=row["group_name"],
                            description=row["description"],
                            related=row.get("related") or [],
                            projects=row.get("projects"),
                            technologies=row.get("technologies"),
                        )
                        for row in nodes_resp.data
                    ]
                    active_ids = {n.id for n in nodes}
                    edges = [
                        GraphEdge(source=row["source"], target=row["target"])
                        for row in (edges_resp.data or [])
                        if row["source"] in active_ids and row["target"] in active_ids
                    ]
                    if not edges:
                        seen: set[str] = set()
                        for node in nodes:
                            for target in node.related:
                                if target not in active_ids:
                                    continue
                                key = "::".join(sorted([node.id, target]))
                                if key not in seen:
                                    seen.add(key)
                                    edges.append(GraphEdge(source=node.id, target=target))
                    return KnowledgeGraphResponse(nodes=nodes, edges=edges)
            except Exception as exc:
                logger.warning("Supabase knowledge graph fetch failed, using static data: %s", exc)

    return static_knowledge_graph()


def get_knowledge_node(node_id: str, settings: Settings | None = None) -> KnowledgeNode | None:
    settings = settings or get_settings()
    if settings.use_supabase_knowledge and settings.supabase_enabled:
        client = get_supabase_client(settings)
        if client:
            try:
                resp = (
                    client.table("knowledge_nodes")
                    .select("*")
                    .eq("id", node_id)
                    .eq("is_active", True)
                    .maybe_single()
                    .execute()
                )
                if resp.data:
                    row = resp.data
                    return KnowledgeNode(
                        id=row["id"],
                        label=row["label"],
                        group=row["group_name"],
                        description=row["description"],
                        related=row.get("related") or [],
                        projects=row.get("projects"),
                        technologies=row.get("technologies"),
                    )
            except Exception as exc:
                logger.warning("Supabase node fetch failed for %s: %s", node_id, exc)

    return knowledge_node_by_id(node_id)
