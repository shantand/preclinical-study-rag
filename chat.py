import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "toxicity_studies"
CHROMA_PATH = "./chroma_db"
TOP_K = 12

client = OpenAI()

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

db = chromadb.PersistentClient(path=CHROMA_PATH)
collection = db.get_collection(COLLECTION_NAME)

print("Ready!\n")

while True:

    question = input("Ask a question (or 'exit'): ")

    if question.lower() == "exit":
        break

    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    retrieved_docs = results["documents"][0]
    retrieved_meta = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n========== Retrieved Chunks ==========\n")

    context = ""

    for i, (doc, meta, distance) in enumerate(
        zip(retrieved_docs, retrieved_meta, distances),
        start=1,
    ):

        print(f"{i}. {meta['source']}")
        print(f"Distance : {distance:.4f}")
        print(doc[:300])
        print("-" * 60)

        context += (
            f"\nSource: {meta['source']}\n"
            f"{doc}\n"
        )

    print("\nGenerating Answer...\n")

    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": (
                    "You are a helpful research assistant.\n"
                    "Answer ONLY using the provided context.\n"
                    "If the answer is not present, clearly say so."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                ),
            },
        ],
    )

    print("========== Answer ==========\n")
    print(response.output_text)
    print()
