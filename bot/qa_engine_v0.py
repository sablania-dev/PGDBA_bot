import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from openai import OpenAI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

class QABot:
    def __init__(self, faq_file="data/faqs.json", index_file="models/embeddings_index.faiss", openai_model=None):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.faqs = json.load(open(faq_file, "r"))
        self.index = faiss.read_index(index_file)
        self.embeddings = self.model.encode([faq["question"] for faq in self.faqs])
        # Use model from config if not provided
        self.openai_model = openai_model or getattr(config, "OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=getattr(config, "OPENAI_API_KEY", None))

    def _openai_chat(self, messages, temperature=0.2, max_tokens=512):
        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    def generate_subqueries(self, user_query):
        prompt = (
            "You are a helpful assistant for a FAQ chatbot. "
            "Given the user's question, generate 1-3 concise subqueries that would help retrieve the most relevant FAQ entries. "
            "Return them as a Python list of strings.\n"
            f"User question: {user_query}"
        )
        messages = [
            {"role": "system", "content": "You generate subqueries for FAQ retrieval."},
            {"role": "user", "content": prompt}
        ]
        subqueries_str = self._openai_chat(messages, temperature=0.1, max_tokens=128)
        try:
            subqueries = eval(subqueries_str)
            if isinstance(subqueries, list):
                return subqueries
        except Exception:
            pass
        return [user_query]

    def retrieve_faqs(self, queries, top_k=2):
        # For each query, retrieve top_k FAQs
        all_results = []
        for q in queries:
            query_emb = self.model.encode([q])
            scores, idx = self.index.search(np.array(query_emb).astype("float32"), top_k)
            for i in range(top_k):
                faq_idx = idx[0][i]
                score = scores[0][i]
                if 0 <= faq_idx < len(self.faqs):
                    all_results.append({
                        "faq": self.faqs[faq_idx],
                        "score": float(score),
                        "query": q
                    })
        # Remove duplicates (by question)
        seen = set()
        unique_results = []
        for r in all_results:
            q = r["faq"]["question"]
            if q not in seen:
                unique_results.append(r)
                seen.add(q)
        # Sort by score descending
        unique_results.sort(key=lambda x: -x["score"])
        return unique_results

    def synthesize_answer(self, user_query, retrieved_faqs):
        context = "\n\n".join([
            f"Q: {r['faq']['question']}\nA: {r['faq']['answer']}" for r in retrieved_faqs
        ])
        prompt = (
            "You are a helpful assistant for a FAQ chatbot. "
            "Given the user's question and the following FAQ context, answer the user's question as accurately as possible. "
            "If the answer is not found, say you don't know. "
            "If a link is present in the FAQ, append it at the end.\n"
            f"User question: {user_query}\n\nFAQ context:\n{context}"
        )
        messages = [
            {"role": "system", "content": "You answer user questions using FAQ context."},
            {"role": "user", "content": prompt}
        ]
        return self._openai_chat(messages, temperature=0.2, max_tokens=512)

    def search(self, query, threshold=0.70, top_k=2):
        # Step 1: Generate subqueries using LLM
        subqueries = self.generate_subqueries(query)
        # Step 2: Retrieve top_k FAQs for each subquery
        retrieved = self.retrieve_faqs(subqueries, top_k=top_k)
        # Step 3: Filter by threshold
        filtered = [r for r in retrieved if r["score"] >= threshold]
        if not filtered:
            filtered = retrieved[:1]  # fallback: at least one
        # Step 4: Synthesize answer using LLM
        answer = self.synthesize_answer(query, filtered)
        return answer, filtered[0]["score"] if filtered else 0.0
