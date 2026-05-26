from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import settings


class ChunkingService:
    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk_text(self, text: str, metadata: dict | None = None) -> list[dict]:
        base_metadata = metadata or {}
        chunks = self.splitter.split_text(text)
        return [
            {
                "text": chunk,
                "metadata": {**base_metadata, "chunk_index": i},
                "chunk_index": i,
            }
            for i, chunk in enumerate(chunks)
        ]


# Singleton
_chunking_service: ChunkingService | None = None


def get_chunking_service() -> ChunkingService:
    global _chunking_service
    if _chunking_service is None:
        _chunking_service = ChunkingService()
    return _chunking_service
