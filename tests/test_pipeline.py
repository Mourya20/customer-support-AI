"""Basic tests for support pipeline."""

from src.pipeline import SupportPipeline


def _pipeline() -> SupportPipeline:
    return SupportPipeline(enable_llm=False)


def test_billing_query_routes_and_answers() -> None:
    result = _pipeline().handle_query("I was charged twice for my subscription.")
    assert result["category"] == "billing"
    assert result["escalate"] is False
    assert "billing" in result["answer"].lower()
    assert result["sources"]


def test_technical_query_routes_and_answers() -> None:
    result = _pipeline().handle_query("My application keeps returning a 500 error.")
    assert result["category"] == "technical"
    assert result["escalate"] is False
    assert "technical" in result["answer"].lower()


def test_out_of_scope_query_escalates() -> None:
    result = _pipeline().handle_query("Can you tell me today's weather in Guntur?")
    assert result["escalate"] is True
    assert "outside supported categories" in result["escalation_reason"].lower()
