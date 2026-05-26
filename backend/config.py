from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Multi-Modal RAG Assistant"
    DEBUG: bool = False

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_VISION_MODEL: str = "llama3.2-vision"

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "documents"

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    # RAG
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    RETRIEVAL_TOP_K: int = 10
    RERANK_TOP_K: int = 5

    # Security
    REQUIRE_API_KEY: bool = False
    API_KEY: str = ""
    MAX_UPLOAD_SIZE_MB: int = 50

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/db/app.db"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Upload
    UPLOAD_DIR: str = "./data/uploads"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
