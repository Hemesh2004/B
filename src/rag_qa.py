import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(df):
    docs = []
    
    # Convert each booking record into a text string
    for idx, row in df.iterrows():
        doc = (
            f"Hotel: {row['hotel']}, "
            f"Arrival Date: {row['arrival_date_month']} {row['arrival_date_year']}, "
            f"ADR: {row['adr']}, "
            f"Country: {row['country']}, "
            f"Revenue: {row['revenue']}, "
            f"Lead Time: {row['lead_time']}"
        )
        docs.append(doc)

    # Generate embeddings for all docs
    embeddings = model.encode(docs, show_progress_bar=True)

    # Convert to NumPy array for FAISS
    embeddings = np.array(embeddings)

    # Create FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, docs

def search(query, index, docs, top_k=3):
    # Generate query embedding
    query_embedding = model.encode([query])

    # Perform search
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Return matched documents
    results = [docs[idx] for idx in indices[0]]
    return results

if __name__ == "__main__":
    from data_preprocessing import load_and_clean_data

    # Load the data
    df = load_and_clean_data('data/hotel_bookings.csv')

    print("Creating embeddings and building FAISS index...")
    index, docs = create_embeddings(df)
    print("Index built successfully!")

    # Example query
    query = "Bookings from Portugal"
    print(f"Search Query: {query}")

    results = search(query, index, docs)

    print("Top Results:")
    for res in results:
        print(res)
