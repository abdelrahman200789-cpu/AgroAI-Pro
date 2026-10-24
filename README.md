# AgroAI Pro — IR-Based Agricultural Chatbot

AgroAI Pro is a simple Streamlit chat interface built on the project's existing Information Retrieval (IR) engine. It uses **TF-IDF** and **Cosine Similarity** to retrieve the most relevant agricultural knowledge notes for a user's question.

## What it does

- Provides a clean chat-style interface with conversation history.
- Accepts questions about topics covered in the local knowledge base.
- Ranks notes using TF-IDF vectors and cosine similarity.
- Shows the retrieved answer and related source notes with relevance scores.
- Includes suggested questions and a clear-conversation control.
- Works locally without an API key or generative AI model.

## Important distinction

This is an **information-retrieval chatbot**, not a generative LLM. It does not invent a new answer; it returns the most relevant existing note from `data/knowledge/`. A relevance score measures textual similarity, not truth or scientific certainty. Answer quality depends on the contents and coverage of the knowledge base.

## Requirements

- Python 3.10 or newer
- pip

## Run locally

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app normally opens at `http://localhost:8501`.

## Project structure

```text
AgroAI_Pro_Streamlit/
├── app.py                       # Chat UI built with Streamlit
├── agro_engine.py               # Existing IR engine and project logic
├── data/
│   ├── knowledge/                # Text documents searched by the IR engine
│   ├── crops.csv                 # Existing project data
│   └── disease_rules.json        # Existing project data
├── tests/
│   └── test_agro_engine.py
├── requirements.txt
├── REPORT.md
└── .gitignore
```

## How retrieval works

1. The app reads the `.txt` notes from `data/knowledge/`.
2. `TfidfVectorizer` turns each note into a numerical vector.
3. The user's question is transformed with the same vectorizer.
4. `cosine_similarity` compares the question vector with the note vectors.
5. The app shows the highest-ranked note and up to two related notes.

## Extend the knowledge base

Add a `.txt` file inside `data/knowledge/`. Keep it focused on one topic and use clear, descriptive language. The IR engine automatically includes `.txt` files in that folder during a search.

## Limitations

- The knowledge base is small and educational, so some questions will not have a matching answer.
- The current vectorizer is configured for English text; Arabic questions may not retrieve relevant notes reliably.
- The app is not a substitute for professional agricultural advice.

## Testing

```bash
pytest -q
```

## Deployment

The app can be deployed on Streamlit Community Cloud by connecting the GitHub repository, selecting the intended branch, and setting `app.py` as the main file.
