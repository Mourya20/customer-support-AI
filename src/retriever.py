"""Knowledge base retrieval module."""

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class RetrievedChunk:
    title: str
    content: str
    score: float


class TfidfRetriever:
    def __init__(self, kb_path: str, top_k: int = 3) -> None:
        self.kb_path = Path(kb_path)
        self.top_k = top_k
        self.chunks = self._load_chunks(self.kb_path)

        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.chunk_vectors = self.vectorizer.fit_transform(
            [f"{chunk.title}\n{chunk.content}" for chunk in self.chunks]
        )

    def _load_chunks(self, kb_path: Path) -> List[RetrievedChunk]:
        text = kb_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        chunks: List[RetrievedChunk] = []
        current_title = "General"
        current_content: List[str] = []

        def flush_chunk() -> None:
            nonlocal current_title, current_content
            content = "\n".join(current_content).strip()
            if content:
                chunks.append(RetrievedChunk(title=current_title, content=content, score=0.0))
            current_content = []

        for line in lines:
            if line.startswith("### "):
                flush_chunk()
                current_title = line.replace("### ", "").strip()
            elif line.startswith("## "):
                flush_chunk()
                current_title = line.replace("## ", "").strip()
            elif line.startswith("# "):
                continue
            else:
                current_content.append(line)

        flush_chunk()

        if not chunks:
            raise ValueError("Knowledge base contains no retrievable chunks")

        return chunks

    def retrieve(self, query: str, category_hint: str | None = None) -> List[RetrievedChunk]:
        query_vector = self.vectorizer.transform([query])
        scores = (self.chunk_vectors @ query_vector.T).toarray().ravel()

        ranked_indices = np.argsort(scores)[::-1]
        selected: List[RetrievedChunk] = []

        normalized_hint = None
        if category_hint and category_hint != "unknown":
            normalized_hint = category_hint.replace("_", " ").lower()

        for idx in ranked_indices:
            chunk = self.chunks[idx]
            score = float(scores[idx])
            if score <= 0:
                continue
            if normalized_hint and normalized_hint not in chunk.title.lower():
                if len(selected) == 0:
                    # keep searching for a category-aligned first chunk
                    continue
            selected.append(
                RetrievedChunk(title=chunk.title, content=chunk.content, score=round(score, 3))
            )
            if len(selected) >= self.top_k:
                break

        if not selected:
            fallback_indices = np.argsort(scores)[::-1][: self.top_k]
            for idx in fallback_indices:
                if scores[idx] <= 0:
                    continue
                chunk = self.chunks[idx]
                selected.append(
                    RetrievedChunk(
                        title=chunk.title,
                        content=chunk.content,
                        score=round(float(scores[idx]), 3),
                    )
                )

        return selected
