<<<<<<< HEAD

=======
# AgroAI Pro — Project Report

## 1. Project overview

AgroAI Pro is an agricultural information-retrieval chatbot. Its purpose is to let users ask questions in a chat interface and retrieve relevant information from a collection of local agricultural text notes.

## 2. Problem statement

Agricultural information in separate documents can be inconvenient to search manually. This prototype offers one chat-style entry point and ranks existing notes against a user's question.

## 3. Objectives

- Reuse the project's IR engine rather than train a machine-learning model from scratch.
- Present the retrieval workflow through a simple, polished Streamlit chat UI.
- Return relevant local notes and make the source files visible to users.
- Keep the system lightweight and runnable without API keys or a generative model.

## 4. System architecture

**User question → Streamlit chat interface → TF-IDF vectorization → cosine similarity → ranked local notes → answer and source display**

The interface is implemented in `app.py`. The retrieval logic is implemented in `agro_engine.py`, primarily in `search_knowledge()`. The searchable text files are stored in `data/knowledge/`.

## 5. Information Retrieval method

### TF-IDF

TF-IDF stands for Term Frequency–Inverse Document Frequency. Term frequency reflects how often a term appears in a document, while inverse document frequency reduces the influence of terms that appear across many documents. This produces vectors that emphasize terms useful for distinguishing documents.

### Cosine Similarity

Cosine similarity compares the direction of the query vector with each document vector. The notes are sorted by their similarity score, and the most relevant note is shown first. The score is a text-relevance signal; it is not a probability, factual-confidence score, or measure of scientific validity.

### Response behavior

The app presents the content of the highest-ranked note as the main response and can display up to two related notes. If no note shares usable terms with the query, it asks the user to try different or broader keywords. This is retrieval-based behavior, not generative text creation.

## 6. User interface

The Streamlit interface includes:

- Chat bubbles for the user and assistant.
- Conversation history for the current session.
- Suggested example questions.
- Expandable source details and relevance scores.
- A sidebar that explains the retrieval pipeline.
- A control to clear the conversation.

## 7. Data

The IR engine searches `.txt` files in `data/knowledge/`. The data is a small educational knowledge base covering topics such as irrigation, crop planning, plant disease scouting, integrated pest management, soil pH, and sensor data quality. The system's coverage is limited by the notes that are provided.

## 8. Technologies

- Python
- Streamlit
- scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- Existing project knowledge text files
- pytest for tests

## 9. Limitations

- The chatbot cannot answer reliably if the needed information is missing from the knowledge base.
- The configured vectorizer is intended for English notes and does not provide reliable Arabic retrieval.
- Cosine similarity measures textual overlap, so a high score does not guarantee that the content is correct or directly answers the question.
- No generative LLM, external agricultural API, live sensor connection, or image classifier is part of this version.

## 10. Future improvements

1. Expand the knowledge base with reliable, referenced agricultural sources.
2. Add better query preprocessing and support for synonyms.
3. Evaluate retrieval quality with a test set of questions and expected relevant documents.
4. Consider Arabic-language retrieval with a suitable tokenizer/vectorization strategy.
5. If needed later, add a generative model only as a separate layer grounded in retrieved documents.

## 11. Conclusion

This version focuses on the teammate's proposed scope: reusing the existing TF-IDF and cosine-similarity IR engine and building a chat UI over it. It intentionally excludes image-based diagnosis and unrelated dashboard features so the core project remains clear and easy to demonstrate.
>>>>>>> 5981c57 (Improve AgroAI chat UI and question suggestions)
