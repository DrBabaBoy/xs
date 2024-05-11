import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FaceData(BaseModel):
    doc_id: int = Field(default=None, exclude=True)
    name: str = Field(min_length=1)
    surname: str = Field(default="", min_length=1)
    user_id: Optional[int] = Field(default=None)
    career: Optional[str] = Field(default=None)
    acss: str = Field(default=None)
    data_path: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


if __name__ == "__main__":
    face_data = FaceData(name="test")
    assert face_data.doc_id is None
    face_data.doc_id = 1
    assert face_data.doc_id == 1
