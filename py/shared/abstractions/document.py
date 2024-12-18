"""Abstractions for documents and their extractions."""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from .base import R2RSerializable

logger = logging.getLogger()


class DocumentType(str, Enum):
    """Types of documents that can be stored."""

    # Audio
    MP3 = "mp3"

    # CSV
    CSV = "csv"

    # Email
    EML = "eml"
    MSG = "msg"
    P7S = "p7s"

    # EPUB
    EPUB = "epub"

    # Excel
    XLS = "xls"
    XLSX = "xlsx"

    # HTML
    HTML = "html"
    HTM = "htm"

    # Image
    BMP = "bmp"
    HEIC = "heic"
    JPEG = "jpeg"
    PNG = "png"
    TIFF = "tiff"
    JPG = "jpg"
    SVG = "svg"
    WEBP = "webp"
    ICO = "ico"

    # Markdown
    MD = "md"

    # Org Mode
    ORG = "org"

    # Open Office
    ODT = "odt"

    # PDF
    PDF = "pdf"

    # Plain text
    TXT = "txt"
    JSON = "json"

    # PowerPoint
    PPT = "ppt"
    PPTX = "pptx"

    # reStructured Text
    RST = "rst"

    # Rich Text
    RTF = "rtf"

    # TSV
    TSV = "tsv"

    # Video/GIF
    MP4 = "mp4"
    GIF = "gif"

    # Word
    DOC = "doc"
    DOCX = "docx"

    # XML
    XML = "xml"


class Document(R2RSerializable):
    id: UUID = Field(default_factory=uuid4)
    collection_ids: list[UUID]
    owner_id: UUID
    document_type: DocumentType
    metadata: dict

    class Config:
        arbitrary_types_allowed = True
        ignore_extra = False
        json_encoders = {
            UUID: str,
        }
        populate_by_name = True


class IngestionStatus(str, Enum):
    """Status of document processing."""

    PENDING = "pending"
    PARSING = "parsing"
    EXTRACTING = "extracting"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    AUGMENTING = "augmenting"
    STORING = "storing"
    ENRICHING = "enriching"
    ENRICHED = "enriched"

    FAILED = "failed"
    SUCCESS = "success"

    def __str__(self):
        return self.value

    @classmethod
    def table_name(cls) -> str:
        return "documents"

    @classmethod
    def id_column(cls) -> str:
        return "document_id"


class KGExtractionStatus(str, Enum):
    """Status of KG Creation per document."""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    ENRICHED = "enriched"
    FAILED = "failed"

    def __str__(self):
        return self.value

    @classmethod
    def table_name(cls) -> str:
        return "documents"

    @classmethod
    def id_column(cls) -> str:
        return "id"


class KGEnrichmentStatus(str, Enum):
    """Status of KG Enrichment per collection."""

    PENDING = "pending"
    PROCESSING = "processing"
    OUTDATED = "outdated"
    SUCCESS = "success"
    FAILED = "failed"

    def __str__(self):
        return self.value

    @classmethod
    def table_name(cls) -> str:
        return "collections"

    @classmethod
    def id_column(cls) -> str:
        return "id"


class DocumentResponse(R2RSerializable):
    """Base class for document information handling."""

    id: UUID
    collection_ids: list[UUID]
    owner_id: UUID
    document_type: DocumentType
    metadata: dict
    title: Optional[str] = None
    version: str
    size_in_bytes: Optional[int]
    ingestion_status: IngestionStatus = IngestionStatus.PENDING
    extraction_status: KGExtractionStatus = KGExtractionStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    ingestion_attempt_number: Optional[int] = None
    summary: Optional[str] = None
    summary_embedding: Optional[list[float]] = None  # Add optional embedding

    def convert_to_db_entry(self):
        """Prepare the document info for database entry, extracting certain fields from metadata."""
        now = datetime.now()

        # Format the embedding properly for Postgres vector type
        embedding = None
        if self.summary_embedding is not None:
            embedding = f"[{','.join(str(x) for x in self.summary_embedding)}]"

        return {
            "id": self.id,
            "collection_ids": self.collection_ids,
            "owner_id": self.owner_id,
            "document_type": self.document_type,
            "metadata": json.dumps(self.metadata),
            "title": self.title or "N/A",
            "version": self.version,
            "size_in_bytes": self.size_in_bytes,
            "ingestion_status": self.ingestion_status.value,
            "extraction_status": self.extraction_status.value,
            "created_at": self.created_at or now,
            "updated_at": self.updated_at or now,
            "ingestion_attempt_number": self.ingestion_attempt_number or 0,
            "summary": self.summary,
            "summary_embedding": embedding,
        }


class UnprocessedChunk(R2RSerializable):
    """An extraction from a document."""

    id: Optional[UUID] = None
    document_id: Optional[UUID] = None
    collection_ids: list[UUID] = []
    metadata: dict = {}
    text: str


class UpdateChunk(R2RSerializable):
    """An extraction from a document."""

    id: UUID
    metadata: Optional[dict] = None
    text: str


class DocumentChunk(R2RSerializable):
    """An extraction from a document."""

    id: UUID
    document_id: UUID
    collection_ids: list[UUID]
    owner_id: UUID
    data: str | bytes
    metadata: dict


class RawChunk(R2RSerializable):
    text: str
