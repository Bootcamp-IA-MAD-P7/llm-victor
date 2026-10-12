"""Direct generation workflow using LangGraph."""

from __future__ import annotations

from typing import Any, cast

try:
    from langgraph.graph import END, StateGraph  # type: ignore[import-not-found]
except Exception:  # pragma: no cover
    StateGraph = None
    END = "END"

from ..providers.groq import GroqProvider


def build_direct_graph(provider: GroqProvider | None = None) -> Any:
    """Build LangGraph for direct generation."""

    if provider is None:
        provider = GroqProvider()

    def generate(state: dict[str, Any]) -> dict[str, Any]:
        brief = state.get("brief", "")
        prompt = f"Genera una publicación de LinkedIn basada en este briefing:\n\n{brief}"
        result = provider.generate_text(prompt, model=state.get("model"))
        return result

    if StateGraph is None:
        # Simple non-graph fallback
        class SimpleGraph:
            def __init__(self) -> None:
                pass

            def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
                return generate(state)

        return cast(Any, SimpleGraph())

    graph = StateGraph(dict)
    graph.add_node("generate", generate)
    graph.add_edge("generate", END)
    return graph.compile()


def generate_direct(
    brief: str,
    model: str | None = None,
    provider: GroqProvider | None = None,
) -> dict[str, Any]:
    """Execute direct generation."""
    graph = build_direct_graph(provider)
    result = graph.invoke({"brief": brief, "model": model})
    # Ensure required keys
    if not isinstance(result, dict):
        return {"text": str(result), "provider": "groq", "model": model or "unknown"}
    result.setdefault("provider", "groq")
    result.setdefault("model", model or "llama-3.1-8b-instant")
    result.setdefault("text", result.get("text", ""))
    return result
