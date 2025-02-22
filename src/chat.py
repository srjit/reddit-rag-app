import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import chromadb

# Load Phi-2 model & tokenizer (CPU mode)
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)

# Load ChromaDB
chroma_client = chromadb.PersistentClient(path="../data/chroma_db")
collection = chroma_client.get_collection(name="reddit_posts")

def retrieve_relevant_docs(query, k=3):
    """Fetch top-k relevant documents
       from ChromaDB based on query."""
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results["documents"][0] if results["documents"] else []

def generate_response(query):

    """Retrieve relevant documents and
      generate a response using Phi-2."""
    
    docs = retrieve_relevant_docs(query)
    context = "\n".join(docs) if docs else "No relevant documents found."

    prompt = f"Context:\n{context}\n\nUser: {query}\nAI:"
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=200)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("AI:")[-1].strip()

# Interactive chat loop
print("🧠 RAG Chatbot (using Phi-2 & ChromaDB). Type 'exit' to quit.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Goodbye! 👋")
        break
    
    response = generate_response(user_input)
    print(f"AI: {response}")
