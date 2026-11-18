import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from app.core.database import Base


class ClassificationHistory(Base):
    __tablename__ = "classification_history"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    movie_id = Column(String(128), nullable=False, index=True)
    action = Column(String(64), nullable=False)  # classified, reclassified, corrected
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProcessingStatus(Base):
    __tablename__ = "processing_status"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    movie_id = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="pending")  # pending, processing, done, failed, unclassified
    error_message = Column(Text, nullable=True)
    attempts = Column(String(8), default="0")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
