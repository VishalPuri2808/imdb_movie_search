
# 🎬 IMDB Semantic Movie Recommender

A **semantic search engine** built with **Streamlit**, **Pinecone**, and **Hugging Face Sentence Transformers** to recommend movies based on natural language descriptions. Just describe what kind of movie you're in the mood for — and get intelligent, personalized recommendations from the IMDB Top 1000 dataset.

---

## 🚀 Features

- 🔎 Search by natural language (e.g., "sci-fi adventure with space travel")
- 🤖 Semantic vector embeddings using `all-MiniLM-L6-v2`
- 🧠 Fast cosine similarity search with **Pinecone**
- 🖼️ Clean Streamlit interface with genre, overview, and titles
- 📊 Scalable and deployable as a web app

---

## 📂 Project Structure

```
📁 imdb-semantic-search/
│
├── app.py                  # Main Streamlit app (self-contained)
├── imdb_top_1000.csv       # Input dataset from Kaggle
├── requirements.txt        # Python dependencies
└── README.md               # Project description
```

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/imdb-semantic-search.git
cd imdb-semantic-search
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Python ≥ 3.8 recommended

### 3. Add the Dataset

Download [`imdb_top_1000.csv`](https://www.kaggle.com/datasets) from Kaggle and place it in the root folder.

### 4. Set Your Pinecone API Key

In `app.py`, replace the following line with your actual API key:

```python
PINECONE_API_KEY = "your-pinecone-api-key"
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 🧠 How It Works

| Component       | Description                                                 |
|----------------|-------------------------------------------------------------|
| **Embedding**   | Uses Hugging Face `all-MiniLM-L6-v2` for 384-dim sentence embeddings |
| **Vector DB**   | Pinecone serverless index to store and search movie vectors |
| **Search**      | Cosine similarity-based semantic matching                   |
| **Frontend**    | Built with Streamlit for quick text input and display       |

---

## 🔮 Example Query

> _“A thrilling mystery with unexpected twists and a strong female lead”_

Returns:
- 🎥 *Gone Girl*
- 🎥 *The Girl with the Dragon Tattoo*
- 🎥 *Knives Out*
- ...

---

## 🌍 Deployment Options

- 🟢 [Streamlit Cloud](https://streamlit.io/cloud)
- 💻 [Hugging Face Spaces](https://huggingface.co/spaces)
- ☁️ Host on AWS Lambda + S3 using Docker

---

## ✅ To-Do (Suggestions)

- [ ] Add movie posters using OMDb or TMDB API
- [ ] Add filters by genre and release year
- [ ] Deploy live with Streamlit Cloud
- [ ] Save user searches for feedback/training

---

## 📚 Dataset Info

- Source: [IMDB Top 1000 Movies on Kaggle](https://www.kaggle.com/datasets)
- Fields used: `Series_Title`, `Genre`, `Overview`

---

## 🧑‍💻 Author

**Vishal**  
📍 Texas, USA  
💼 LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)  
✉️ Email: youremail@example.com  

---

## 📜 License

MIT License © 2025 Vishal  
Feel free to use, modify, and share with credit!
