import os
import pandas as pd

# Path to your CSV dataset file
CSV_FILE_PATH = "LaptrackPhase2.csv"

# Embedding model name used for generating embeddings (change if needed)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Chat history storage file
CHAT_HISTORY_FILE = "chat_history.csv"

def filter_data(df, min_price=0, max_price=100000, brands=None):
    """
    Filters the laptop DataFrame based on price range and selected brands.
    """
    filtered = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
    if brands:
        filtered = filtered[filtered['Brand'].isin(brands)]
    return filtered

def save_chat_history(user_query, response):
    """
    Saves a new chat entry to the chat history CSV file.
    """
    history = []
    if os.path.exists(CHAT_HISTORY_FILE):
        history = pd.read_csv(CHAT_HISTORY_FILE).to_dict('records')
    history.append({'Query': user_query, 'Response': response})
    pd.DataFrame(history).to_csv(CHAT_HISTORY_FILE, index=False)

def load_chat_history():
    """
    Loads chat history from CSV file, returns an empty DataFrame if none exists.
    """
    if os.path.exists(CHAT_HISTORY_FILE):
        return pd.read_csv(CHAT_HISTORY_FILE)
    else:
        return pd.DataFrame(columns=['Query', 'Response'])