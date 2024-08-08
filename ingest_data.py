from api.ingestion import ingest

if __name__ == "__main__":
    retriever = ingest()
    print("Data ingested successfully into Qdrant.")
