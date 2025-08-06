from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

# ⬅️ This is what app.py is trying to import
Base = declarative_base()

class RequestLog(Base):
    __tablename__ = 'request_logs'

    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    input_data = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
