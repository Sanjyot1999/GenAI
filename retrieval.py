from embedding_utils import generate_embeddings, create_faiss_index
import numpy as np

def setup_retrieval(df, description_column="Description"):
    texts = df[description_column].astype(str).tolist()
    embeddings = generate_embeddings(texts)
    index = create_faiss_index(np.array(embeddings))
    return index, embeddings

def query_index(index, query, df, top_k=3):
    query_embedding = generate_embeddings([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return df.iloc[indices[0]]