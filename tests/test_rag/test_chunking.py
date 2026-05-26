from rag.chunking import ChunkingService


def test_chunk_short_text():
    service = ChunkingService(chunk_size=100, chunk_overlap=10)
    chunks = service.chunk_text("Short text.", {"doc_id": "test"})

    assert len(chunks) == 1
    assert chunks[0]["text"] == "Short text."
    assert chunks[0]["chunk_index"] == 0
    assert chunks[0]["metadata"]["doc_id"] == "test"


def test_chunk_long_text():
    service = ChunkingService(chunk_size=50, chunk_overlap=10)
    long_text = "This is a sentence. " * 20

    chunks = service.chunk_text(long_text, {"doc_id": "test"})

    assert len(chunks) > 1
    for i, chunk in enumerate(chunks):
        assert chunk["chunk_index"] == i
        assert len(chunk["text"]) > 0


def test_chunk_preserves_metadata():
    service = ChunkingService(chunk_size=100, chunk_overlap=10)
    metadata = {"source": "test", "type": "log"}
    chunks = service.chunk_text("Some content here.", metadata)

    assert chunks[0]["metadata"]["source"] == "test"
    assert chunks[0]["metadata"]["type"] == "log"
    assert chunks[0]["metadata"]["chunk_index"] == 0
