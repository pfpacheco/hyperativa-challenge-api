from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserVO(BaseModel):

    id: Optional[int] = None
    name: str
    is_active: bool
    username: str
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
