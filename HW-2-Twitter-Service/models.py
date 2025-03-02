# Added By: Vatsal Gandhi
from pydantic import BaseModel

class CreatePostRequest(BaseModel):
    content: str

class CreatePostResponse(BaseModel):
    message: str
    id: str
    content: str
    created_at: str

class PostIDsResponse(BaseModel):
    ids: list[str]

class GetPostResponse(BaseModel):
    message: str
    id: str
    content: str
    created_at: str

class DeletePostResponse(BaseModel):
    message: str
    