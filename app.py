import streamlit as st
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# ------------------------ CONFIGURING ------------------------
PINECONE_API_KEY = "pcsk_zZhme_8Cgs51QMWnRtr2WBPqsQNAgGjyDe971vZsCYY9wxQyKgN6HUnA7chJgtxFuyN12"  
INDEX_NAME = "imdb-search"

# ------------------------ SETUP ------------------------
st.set_page_config(page_title="IMDB Semantic Movie Recommender", layout="wide")
st.title("🎬 IMDB Semantic Movie Recommender")

# ------------------------ LOADING MODEL ------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ------------------------ LOADING & EMBEDDING DATA ------------------------
@st.cache_resource
def load_and_embed_data():
    df = pd.read_csv("imdb_top_1000.csv")
    df["embedding_text"] = df["Series_Title"] + " " + df["Overview"]
    df = df.fillna("")
    embeddings = model.encode(df["embedding_text"].tolist(), show_progress_bar=True)
    return df, embeddings

df, embeddings = load_and_embed_data()

# ------------------------ PINECONE INITIALIZATION ------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # all-MiniLM-L6-v2 output size changed from 1024
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west1")
    )

index = pc.Index(INDEX_NAME)

# ------------------------ UPSERT EMBEDDINGS ------------------------
@st.cache_resource
def upsert_embeddings():
    existing_stats = index.describe_index_stats()
    if existing_stats.get("total_vector_count", 0) < len(df):
        to_upsert = [
            {
                "id": str(i),
                "values": embeddings[i].tolist(),
                "metadata": {
                    "title": df["Series_Title"].iloc[i],
                    "genre": df["Genre"].iloc[i],
                    "overview": df["Overview"].iloc[i]
                }
            }
            for i in range(len(df))
        ]
        index.upsert(vectors=to_upsert)
        return f"✅ {len(df)} movie embeddings uploaded."
    else:
        return "✅ Embeddings already upserted."

with st.spinner("Setting up vector database..."):
    status = upsert_embeddings()
    st.success(status)

# ------------------------ QUERY FUNCTION ------------------------
def query_movies(description: str, top_k=5):
    query_embedding = model.encode([description])[0].tolist()
    result = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return result

# ------------------------ STREAMLIT APP UI ------------------------
st.markdown("Enter a description of the kind of movie you want to watch (e.g., 'Sci-fi adventure with space travel')")

user_input = st.text_input("Enter Your movie description:")

if user_input:
    with st.spinner("Searching for recommended movies..."):
        result = query_movies(user_input)

    if result and result.get("matches"):
        st.subheader("Top 5 Recommended Movies:")
        for i, match in enumerate(result["matches"], 1):
            metadata = match["metadata"]
            st.markdown(f"### {i}. 🎞 {metadata['title']}")
            st.markdown(f"**Genre:** {metadata['genre']}")
            st.markdown(f"**Overview:** {metadata['overview']}")
            st.markdown("---")
    else:
        st.warning("❌ No similar movies found. Try a more detailed description.")
