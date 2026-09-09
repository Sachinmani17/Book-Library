from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Query, Response, status
from app.database import get_collection
from app.models import BookCreate, BookResponse, BookUpdate
router = APIRouter(prefix="/books", tags=["Books"])
def serialize_book(book_doc: dict) -> BookResponse:
book_doc["id"] = str(book_doc.pop("_id"))
return BookResponse(**book_doc)
def parse_object_id(book_id: str) -> ObjectId:
try:
return ObjectId(book_id)
except (InvalidId, TypeError):
raise HTTPException(
status_code=status.HTTP_400_BAD_REQUEST,
detail=f"Invalid book ID format: '{book_id}'"
)
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
collection = get_collection()
book_dict = book.model_dump()
result = await collection.insert_one(book_dict)
created_book = await collection.find_one({"_id": result.inserted_id})
return serialize_book(created_book)
@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def list_books(
genre: Optional[str] = Query(default=None, description="Filter by genre"),
in_stock: Optional[bool] = Query(default=None, description="Filter by stock status"),
skip: int = Query(default=0, ge=0, description="Offset for pagination"),
limit: int = Query(default=20, ge=1, le=100, description="Limit for pagination")
):
collection = get_collection()
filters = {}
if genre is not None:
filters["genre"] = {"$regex": f"^{genre}$", "$options": "i"}
if in_stock is not None:
filters["in_stock"] = in_stock
cursor = collection.find(filters).skip(skip).limit(limit)
books = await cursor.to_list(length=limit)
return [serialize_book(doc) for doc in books]
@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: str):
collection = get_collection()
oid = parse_object_id(book_id)
book = await collection.find_one({"_id": oid})
if not book:
raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail=f"Book with id '{book_id}' not found"
)
return serialize_book(book)
@router.put("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book(book_id: str, update_data: BookUpdate):
collection = get_collection()
oid = parse_object_id(book_id)
payload = update_data.model_dump(exclude_unset=True)
if not payload:
raise HTTPException(
  status_code=status.HTTP_400_BAD_REQUEST,
detail="At least one field must be provided for update"
)
result = await collection.update_one({"_id": oid}, {"$set": payload})
if result.matched_count == 0:
raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail=f"Book with id '{book_id}' not found"
)
updated_book = await collection.find_one({"_id": oid})
return serialize_book(updated_book)
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
collection = get_collection()
oid = parse_object_id(book_id)
result = await collection.delete_one({"_id": oid})
if result.deleted_count == 0:
raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail=f"Book with id '{book_id}' not found"
)
return Response(status_code=status.HTTP_204_NO_CONTENT)
