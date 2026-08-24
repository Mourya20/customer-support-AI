"""End-to-end support pipeline module."""

from pathlib import Path
from typing import Any, Dict, Optional

from src.classifier import QueryClassifier
from src.escalation import EscalationHandler
from src.generator import GroundedGenerator
from src.retriever import TfidfRetriever


class SupportPipeline:
    def __init__(self, kb_path: Optional[str] = None, enable_llm: bool = True) -> None:
        root_dir = Path(__file__).resolve().parents[1]
        resolved_kb_path = kb_path or str(root_dir / "data" / "knowledge_base.md")

        self.classifier = QueryClassifier()
        self.retriever = TfidfRetriever(resolved_kb_path)
        self.generator = GroundedGenerator(enable_llm=enable_llm)
        self.escalation = EscalationHandler()

    def handle_query(self, query: str) -> Dict[str, Any]:
        classification = self.classifier.classify(query)
        chunks = self.retriever.retrieve(query, classification.category)
        escalation = self.escalation.evaluate(
            category=classification.category,
            classification_confidence=classification.confidence,
            retrieved_chunks=chunks,
        )

        if escalation.should_escalate:
            return {
                "query": query,
                "category": classification.category,
                "classification_confidence": classification.confidence,
                "escalate": True,
                "escalation_reason": escalation.reason,
                "answer": "ESCALATION REQUIRED",
                "sources": [chunk.title for chunk in chunks],
                "retrieval_scores": [chunk.score for chunk in chunks],
            }

        answer = self.generator.generate(query, classification.category, chunks)

        return {
            "query": query,
            "category": classification.category,
            "classification_confidence": classification.confidence,
            "escalate": False,
            "escalation_reason": escalation.reason,
            "answer": answer,
            "sources": [chunk.title for chunk in chunks],
            "retrieval_scores": [chunk.score for chunk in chunks],
        }
