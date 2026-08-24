"""Escalation logic module."""

from dataclasses import dataclass
from typing import List

from src.retriever import RetrievedChunk


@dataclass
class EscalationDecision:
    should_escalate: bool
    reason: str


class EscalationHandler:
    def __init__(self, classification_threshold: float = 0.6, retrieval_threshold: float = 0.08) -> None:
        self.classification_threshold = classification_threshold
        self.retrieval_threshold = retrieval_threshold

    def evaluate(
        self,
        category: str,
        classification_confidence: float,
        retrieved_chunks: List[RetrievedChunk],
    ) -> EscalationDecision:
        if category == "unknown":
            return EscalationDecision(
                should_escalate=True,
                reason="Query is outside supported categories (Billing, Technical, Account Access).",
            )

        if classification_confidence < self.classification_threshold:
            return EscalationDecision(
                should_escalate=True,
                reason="Classification confidence is too low to provide a safe automated answer.",
            )

        if not retrieved_chunks:
            return EscalationDecision(
                should_escalate=True,
                reason="No relevant knowledge base context was retrieved for this query.",
            )

        top_score = max(chunk.score for chunk in retrieved_chunks)
        if top_score < self.retrieval_threshold:
            return EscalationDecision(
                should_escalate=True,
                reason="Retrieved context confidence is low, so a human agent should review.",
            )

        return EscalationDecision(
            should_escalate=False,
            reason="No escalation needed.",
        )
