from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
def get_current_year() -> int:
return datetime.now().year
class BookBase(BaseModel):
title: str = Field(..., min_length=1, description="Book title is required")
author: str = Field(..., min_length=1, description="Author name is required")
genre: Optional[str] = Field(default=None, description="Optional genre")
year: int = Field(..., description="Publication year")
in_stock: bool = Field(default=True, description="Stock status, defaults to True")
@field_validator("year")
@classmethod
def validate_year(cls, value: int) -> int:
curr_year = get_current_year()
if value <= 1000 or value > curr_year:
raise ValueError(f"Year must be > 1000 and <= {curr_year}")
return value
class BookCreate(BookBase):
pass
class BookUpdate(BaseModel):
title: Optional[str] = Field(default=None, min_length=1)
author: Optional[str] = Field(default=None, min_length=1)
genre: Optional[str] = None
year: Optional[int] = None
in_stock: Optional[bool] = None
@field_validator("year")
@classmethod
def validate_year(cls, value: Optional[int]) -> Optional[int]:
if value is None:
return value
curr_year = get_current_year()
if value <= 1000 or value > curr_year:
raise ValueError(f"Year must be > 1000 and <= {curr_year}")
return value
class BookResponse(BookBase):
id: str = Field(..., description="MongoDB ObjectId string representation")
model_config = {
"json_schema_extra": {
"example": {
"id": "664f1b2c4f1a23456789abcd",
"title": "Clean Architecture",
"author": "Robert C. Martin",
"genre": "Software Engineering",
"year": 2017,
"in_stock": True
}
}
}
