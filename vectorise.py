import json

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "output/chunks.json"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "toxicity_studies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def main():
    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Embedding Dimension: {model.get_sentence_embedding_dimension()}")

    print("Loading chunks...")
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete existing collection (makes reruns easy)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    print("\nCreating embeddings...\n")

    for i, chunk in enumerate(chunks, start=1):

        embedding = model.encode(chunk["text"]).tolist()

        collection.add(
            ids=[str(chunk["id"])],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "char_start": chunk["char_start"],
                "char_end": chunk["char_end"]
            }]
        )

        if i % 25 == 0 or i == len(chunks):
            print(f"Indexed {i}/{len(chunks)} chunks")

    print("\n===================================")
    print("Vectorization Complete")
    print(f"Collection : {COLLECTION_NAME}")
    print(f"Chunks     : {collection.count()}")
    print("===================================")


if __name__ == "__main__":
    main()
