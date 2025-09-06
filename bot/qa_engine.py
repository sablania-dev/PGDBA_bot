import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


class QABot:
    FINAL_PROMPT_TEMPLATE = (
    "You are Kshitish The Chatbot, a PGDBA admissions FAQ assistant, made to help prospective students. Sarthak Sablania, PGDBA Batch-10 student, created you. "
    "Try to use the provided context to answer as much as possible. You don't have to use all of it, just what seems relevant. "
    "If the context does not contain the answer, respond exactly with: 'I don't know based on the available context.'\n"
    "USER QUESTION: {user_query}\n\nCONTEXT:\n{context}"
    )


    def __init__(self, context_file="data/context_document.txt", index_file="models/embeddings_index.faiss", gemini_model=None):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        # Read context document and split into paragraphs
        with open(context_file, "r", encoding="utf-8") as f:
            text = f.read()
        # Split on double newlines or section headers
        self.context_chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        # For embedding, use only the first line of each paragraph
        self.chunk_titles = [chunk.splitlines()[0].strip() if chunk.splitlines() else chunk for chunk in self.context_chunks]
        self.embeddings = self.model.encode(self.chunk_titles)

        # Use Gemini
        genai.configure(api_key=getattr(config, "GEMINI_API_KEY", None))
        self.gemini_model = gemini_model or getattr(config, "GEMINI_MODEL", "gemini-1.5-flash")

    def _gemini_chat(self, messages, temperature=0.2, max_tokens=512):
        """
        messages is a list of dicts like:
        [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        We'll concatenate them into a single prompt since Gemini expects plain text.
        """
        prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        print("[Gemini] Prompt:", prompt)
        model = genai.GenerativeModel(self.gemini_model)
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            print("[Gemini] Response:", response.text.strip())
            return response.text.strip()
        except Exception as e:
            print("[Gemini] Error:", e)
            return "❌ Sorry, there was an error with the Gemini API."

    # Subquery generation removed for simplicity

    def retrieve_context(self, query, top_k=3):
        # Embedding similarity search: embed query, compare to chunk_titles
        query_emb = self.model.encode([query])
        print("[DEBUG] Query for similarity:", query)
        sims = cosine_similarity(query_emb, self.embeddings)[0]
        for i, (title, sim) in enumerate(zip(self.chunk_titles, sims)):
            print(f"[DEBUG] Chunk {i} title for similarity: {title} | Similarity: {sim:.4f}")
        top_indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in top_indices:
            results.append({
                "chunk": self.context_chunks[idx],  # Return full paragraph as context
                "score": float(sims[idx]),
                "query": query
            })
        return results

    def synthesize_answer(self, user_query, retrieved_chunks):
        context = "\n\n".join([r['chunk'] for r in retrieved_chunks])
        prompt = self.FINAL_PROMPT_TEMPLATE.format(user_query=user_query, context=context)
        messages = [
            {"role": "system", "content": "You answer user questions using the provided context."},
            {"role": "user", "content": prompt}
        ]
        print("[Gemini] Synthesizing answer with context:", context)
        return self._gemini_chat(messages, temperature=0.2, max_tokens=512)

    def search(self, query, threshold=0.70, top_k=2):
        retrieved = self.retrieve_context(query, top_k=top_k)

        # Keep only those above threshold
        filtered = [r for r in retrieved if r["score"] >= threshold]

        if not filtered:
            # No sufficiently relevant chunk found → return "don't know"
            return "I don't know based on the available context.", 0.0

        # Otherwise, synthesize with Gemini
        answer = self.synthesize_answer(query, filtered)
        return answer, filtered[0]["score"]

