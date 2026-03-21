# Wk 7 TF Task Submission

The core concept students needed to understand was how a RAG (retrieval-augmented generation) system works, including query-to-text matching, scoring relevant results, and applying guardrails to prevent incorrect or misleading outputs.

Students are most likely to struggle with environment setup, particularly configuring environment variables and installing missing dependencies that are not clearly outlined in the provided instructions. Another common issue is documents not loading correctly, which can break the entire pipeline without obvious errors. AI tools were helpful for troubleshooting technical issues, such as identifying missing requirements or bugs, but could also be proposing solutions that don’t fix the local environment issue and I have to resolve them myself. For example, Claude tried to give me code to read the docs path correctly but it didn’t work so I had to replace a default “docs” path with a local file path resolved one issue but it may not be the most robust solution. Students may also find it challenging to design effective guardrails for handling irrelevant or off-topic queries. 

To guide a student without giving the answer, I would prompt them to revisit the full pipeline step-by-step, asking targeted questions about each stage and encouraging the use of debugging strategies like print statements to verify where the process is failing.




# DocuBot

DocuBot is a small documentation assistant that helps answer developer questions about a codebase.  
It can operate in three different modes:

1. **Naive LLM mode**  
   Sends the entire documentation corpus to a Gemini model and asks it to answer the question.

2. **Retrieval only mode**  
   Uses a simple indexing and scoring system to retrieve relevant snippets without calling an LLM.

3. **RAG mode (Retrieval Augmented Generation)**  
   Retrieves relevant snippets, then asks Gemini to answer using only those snippets.

The docs folder contains realistic developer documents (API reference, authentication notes, database notes), but these files are **just text**. They support retrieval experiments and do not require students to set up any backend systems.

---

## Setup

### 1. Install Python dependencies

    pip install -r requirements.txt

### 2. Configure environment variables

Copy the example file:

    cp .env.example .env

Then edit `.env` to include your Gemini API key:

    GEMINI_API_KEY=your_api_key_here

If you do not set a Gemini key, you can still run retrieval only mode.

---

## Running DocuBot

Start the program:

    python main.py

Choose a mode:

- **1**: Naive LLM (Gemini reads the full docs)  
- **2**: Retrieval only (no LLM)  
- **3**: RAG (retrieval + Gemini)

You can use built in sample queries or type your own.

---

## Running Retrieval Evaluation (optional)

    python evaluation.py

This prints simple retrieval hit rates for sample queries.

---

## Modifying the Project

You will primarily work in:

- `docubot.py`  
  Implement or improve the retrieval index, scoring, and snippet selection.

- `llm_client.py`  
  Adjust the prompts and behavior of LLM responses.

- `dataset.py`  
  Add or change sample queries for testing.

---

## Requirements

- Python 3.9+
- A Gemini API key for LLM features (only needed for modes 1 and 3)
- No database, no server setup, no external services besides LLM calls
