import json
import chromadb
from sentence_transformers import SentenceTransformer

data_file = "../data/reddit_data.json"

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="../data/chroma_db")  # Persistent storage
collection = chroma_client.get_or_create_collection(name="reddit_posts")

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def store_embeddings():

    posts = []
    
    with open(data_file, "r", encoding="utf-8") as f:
        posts = json.loads(f.read())

        
    for post in posts:

        # Text to embed (Title + Body + All Comments)
        texts = [post["title"] + " " + post["selftext"]]
        texts.extend([comment["body"] for comment in post["comments"]])

        embeddings = model.encode(texts, convert_to_numpy=True).tolist()

        # Store each text separately in ChromaDB
        for i, text in enumerate(texts):
            collection.add(
                ids=[f"{post['id']}-{i}"],
                embeddings=[embeddings[i]],
                documents=[text],
                metadatas=[{"post_id": post["id"],
                            "type": "comment" if i > 0 else "post"}]
            )

# Run the embedding and storage process
store_embeddings()
print("Embeddings stored in ChromaDB successfully!")
