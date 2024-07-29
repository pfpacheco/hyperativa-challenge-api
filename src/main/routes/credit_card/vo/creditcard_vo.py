from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class HeaderVO(BaseModel):

    id: Optional[int] = None
    name: str
    date: str
    batch_name: str
    registers: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ItemVO(BaseModel):

    id: Optional[int] = None
    header_id: Optional[int] = None
    line: int
    batch_number: int
    credit_card_number: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
