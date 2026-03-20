"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob
import re  # added for section splitting


class DocuBot:
    def __init__(self, docs_folder="ai110-module4tinker-docubot-starter/docs", llm_client=None): #docs
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory 
        self.documents = self.load_documents()  # List of (filename, text)

        print(f"Loaded {len(self.documents)} documents from {self.docs_folder}.")

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def split_into_sections(self, text):
        """Split document text into sections at ## or ### header boundaries."""
        lines = text.split('\n')
        sections = []
        current = []
        for line in lines:
            if re.match(r'^#{2,}\s', line) and current:
                sections.append('\n'.join(current))
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append('\n'.join(current))
        return [s for s in sections if s.strip()]
    

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []

        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                sections = self.split_into_sections(text)
                for section in sections:
                    docs.append((filename, section))
        
        return docs

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        TODO (Phase 1):
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.

        Example structure:
        {
            "token": ["AUTH.md", "API_REFERENCE.md"],
            "database": ["DATABASE.md"]
        }

        Keep this simple: split on whitespace, lowercase tokens,
        ignore punctuation if needed.
        """
        index = {}
        
        for filename, text in documents:
            words = text.strip().split()
            for word in words:
                word = word.lower()
                if word not in index:
                    index[word] = set()
                index[word].add(filename)

        return index

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    
    def score_document(self, query, section_text, filename=""):
        """
        TODO (Phase 1):
        Return a simple relevance score and section text for how well the text matches the query.

        Suggested baseline:
        - Convert query into lowercase words
        - Count how many appear in the text
        - Return the count as the score
        """
        STOP_WORDS = {"how", "do", "i", "the", "a", "an", "is", "what", "where",
                      "when", "why", "can", "to", "in", "of", "and", "or", "my",
                      "me", "it", "this", "that", "for", "with", "are", "does"}
        score = 0
        query_words = [w.lower() for w in query.strip().split() if w.lower() not in STOP_WORDS]
        text_words = set(section_text.lower().split())
        for word in query_words:
            if word in text_words:
                score += 1

        filename_stem = os.path.splitext(filename)[0].lower()
        for word in query_words:
            if word in filename_stem:
                score += 2

        # for word in query_words:
        #     word = word.lower()
        #     if word in text_words:
        #         score += 1
        return score


    def retrieve(self, query, top_k=3):
        """
        TODO (Phase 1):
        Use the index and scoring function to select top_k relevant document snippets.

        Return a list of (filename, text) sorted by score descending.
        """
        results = []
        for filename, section in self.documents:
            score = self.score_document(query, section, filename)
            if score > 0:
                results.append((filename, section, score))
        results.sort(key=lambda x: x[2], reverse=True)

        return [(filename, section) for filename, section, _ in results[:top_k]]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        source_num = 0
        for filename, text in snippets:
            source_num +=1
            formatted.append(f"✅ Source# {source_num}: [{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
