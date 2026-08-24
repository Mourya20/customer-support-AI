"""Query classification module."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ClassificationResult:
    category: str
    confidence: float
    scores: Dict[str, float]


class QueryClassifier:
    def __init__(self) -> None:
        self.category_keywords: Dict[str, List[str]] = {
            "billing": [
                "bill",
                "billing",
                "charged",
                "charge",
                "refund",
                "payment",
                "invoice",
                "subscription",
            ],
            "technical": [
                "error",
                "500",
                "bug",
                "crash",
                "latency",
                "slow",
                "not loading",
                "timeout",
                "server",
            ],
            "account_access": [
                "login",
                "log in",
                "password",
                "reset",
                "locked",
                "2fa",
                "authentication",
                "account",
            ],
        }

    def classify(self, query: str) -> ClassificationResult:
        lowered = query.lower()
        scores: Dict[str, float] = {}

        for category, keywords in self.category_keywords.items():
            match_count = sum(1 for keyword in keywords if keyword in lowered)
            scores[category] = match_count / max(len(keywords), 1)

        best_category = max(scores, key=scores.get)
        raw_confidence = scores[best_category]

        if raw_confidence == 0:
            return ClassificationResult(category="unknown", confidence=0.0, scores=scores)

        confidence = min(0.55 + raw_confidence, 0.98)
        return ClassificationResult(
            category=best_category,
            confidence=round(confidence, 2),
            scores=scores,
        )
