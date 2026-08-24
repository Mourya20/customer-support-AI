"""Grounded answer generation module."""

import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from src.retriever import RetrievedChunk

load_dotenv()


class GroundedGenerator:
    def __init__(self, enable_llm: bool = True) -> None:
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enable_llm = enable_llm
        self.client = OpenAI(api_key=self.api_key) if (self.api_key and enable_llm) else None

    def _build_context(self, chunks: List[RetrievedChunk]) -> str:
        context_parts = []
        for idx, chunk in enumerate(chunks, start=1):
            context_parts.append(
                f"Source {idx} - {chunk.title} (score: {chunk.score})\n{chunk.content}"
            )
        return "\n\n".join(context_parts)

    def generate(self, query: str, category: str, chunks: List[RetrievedChunk]) -> str:
        context = self._build_context(chunks)

        if not self.client:
            top_source = chunks[0].title if chunks else "knowledge base"
            return (
                f"This appears to be a {category.replace('_', ' ')} request. "
                f"Based on '{top_source}', follow the documented troubleshooting or policy steps "
                "and confirm the result with the customer."
            )

        system_prompt = (
            "You are a customer support assistant. Answer only using the provided knowledge base context. "
            "If context is insufficient, clearly say that more details are needed and recommend escalation."
        )

        user_prompt = (
            f"Customer query: {query}\n"
            f"Classified category: {category}\n\n"
            f"Knowledge base context:\n{context}\n\n"
            "Provide a concise, actionable answer grounded in the context above."
        )

        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        return response.output_text.strip()
