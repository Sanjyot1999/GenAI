# 💻 GenAI-Powered Laptop Recommender App

Welcome to the **GenAI Laptop Recommender**, a smart assistant that helps users find the best laptops based on their profession, use case, and preferences. This app uses Generative AI (via Ollama), semantic search with FAISS, and Streamlit for a friendly and interactive user experience.

---

## 🚀 Project Overview

This project is designed to assist users in choosing laptops based on profession-related queries (e.g., "I'm a data analyst, suggest me a laptop for Python, Excel, and Tableau"). It combines a GenAI chatbot with a searchable laptop database to recommend the best product available.

---

## 🧠 Technologies Used

- **Python**
- **Streamlit** – UI framework for rapid app development.
- **FAISS** – Vector store for similarity search.
- **Ollama (LLM)** – Local LLM for generating answers.
- **HuggingFace Transformers** – To generate embeddings.
- **Pandas** – Data handling.
- **Sentence Transformers** – For semantic text embedding.
- **LaptrackPhase2.csv** – Dataset of laptop specifications.

---

## 📂 Project Structure

```text
├── app.py                # Main Streamlit app
├── config.py             # Centralized configuration
├── data_loader.py        # Loads laptop data from CSV
├── embedding_utils.py    # Embeds laptop descriptions
├── retrieval.py          # Search & filtering logic
├── llm_services.py       # Handles AI responses (Ollama)
├── LaptrackPhase2.csv    # Laptop dataset
└── README.md             # Project documentation


🔧 How Each File Works
app.py
Streamlit-based interface with tabbed views: Search, History, Feedback.

Includes sidebar filters (brand, price range, RAM, storage).

Displays AI suggestions and lets users rate results.

config.py
Holds model names, prompt templates, and other configuration values.

data_loader.py
Loads and preprocesses the laptop data from the CSV file.

embedding_utils.py
Converts laptop descriptions into vector embeddings using Sentence Transformers.

Indexes them in FAISS for fast similarity search.

retrieval.py
Performs query-based search using the FAISS index.

Supports additional filtering logic (e.g., price range, brand).

llm_services.py
Interfaces with Ollama to generate AI suggestions based on user queries.

💡 Features
🔎 Search Assistant: Ask profession-based questions and get personalized laptop suggestions.

⚙️ Sidebar Filters: Filter by price, brand, RAM, and storage.

🧠 AI Suggestions: Get AI-generated recommendations using Ollama.

📝 Chat History: View your previous searches in the "History" tab.

📣 Feedback Tab: Leave feedback and rate the AI responses.

🌓 Dark Mode Support: Interface adapts to Streamlit's dark theme.

🖼️ Product Images and Brand Logos: Displayed alongside suggestions.

📥 Export Feature: Export recommendations as PDF or CSV (optional add-on).