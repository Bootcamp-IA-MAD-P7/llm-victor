"""Direct generation workflow using LangGraph."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, cast

try:
    from langgraph.graph import END, StateGraph  # type: ignore[import-not-found]
except Exception:  # pragma: no cover
    StateGraph = None
    END = "END"

from ..providers.groq import GroqProvider


class Audience(StrEnum):
    """Audience a generation can target."""

    TECH_PROFESSIONALS = "tech-professionals"
    AI_SPECIALISTS = "ai-specialists"
    BUSINESS_LEADERS = "business-leaders"
    GENERAL_AUDIENCE = "general-audience"


class Tone(StrEnum):
    """Tone a generation can use."""

    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    INSPIRING = "inspiring"
    EDUCATIONAL = "educational"


AUDIENCE_LABELS: dict[Audience, str] = {
    Audience.TECH_PROFESSIONALS: "profesionales de tecnología",
    Audience.AI_SPECIALISTS: "especialistas en IA",
    Audience.BUSINESS_LEADERS: "líderes y directivos",
    Audience.GENERAL_AUDIENCE: "público general",
}

TONE_LABELS: dict[Tone, str] = {
    Tone.PROFESSIONAL: "profesional",
    Tone.FRIENDLY: "cercano",
    Tone.INSPIRING: "inspirador",
    Tone.EDUCATIONAL: "divulgativo",
}


def build_prompt(brief: str, audience: Audience, tone: Tone) -> str:
    """Compose the generation prompt from the briefing and its configuration."""
    return (
        "Genera una publicación de LinkedIn basada en este briefing.\n"
        f"Audiencia: {AUDIENCE_LABELS[audience]}\n"
        f"Tono: {TONE_LABELS[tone]}\n\n"
        f"Briefing:\n{brief}"
    )


def build_direct_graph(provider: GroqProvider | None = None) -> Any:
    """Build LangGraph for direct generation."""

    if provider is None:
        provider = GroqProvider()

    def generate(state: dict[str, Any]) -> dict[str, Any]:
        prompt = build_prompt(
            str(state.get("brief", "")),
            cast(Audience, state.get("audience")),
            cast(Tone, state.get("tone")),
        )
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
    audience: Audience,
    tone: Tone,
    model: str | None = None,
    provider: GroqProvider | None = None,
) -> dict[str, Any]:
    """Execute direct generation."""
    graph = build_direct_graph(provider)
    result = graph.invoke({"brief": brief, "audience": audience, "tone": tone, "model": model})
    # Ensure required keys
    if not isinstance(result, dict):
        return {"text": str(result), "provider": "groq", "model": model or "unknown"}
    result.setdefault("provider", "groq")
    result.setdefault("model", model or "llama-3.1-8b-instant")
    result.setdefault("text", result.get("text", ""))
    return result
