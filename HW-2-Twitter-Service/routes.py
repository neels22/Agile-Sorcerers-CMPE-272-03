from fastapi import APIRouter, HTTPException
from service import create_mastodon_post, get_mastodon_post, delete_mastodon_post, get_all_post_ids
from models import CreatePostRequest, CreatePostResponse, PostIDsResponse, GetPostResponse, DeletePostResponse

router = APIRouter()

# Added By: Vatsal Gandhi
@router.post("/post", response_model=CreatePostResponse)
async def create_post(post_request: CreatePostRequest):
    content = post_request.content
    result = await create_mastodon_post(content)
    
    if not result:
        raise HTTPException(status_code=500, detail="Failed to create post")

    return CreatePostResponse(
        message="Post created successfully",
        id=result["id"],
        content=result["content"][3:-4],
        created_at=result["created_at"], 
    )

# Added By: Harishita Gupta
@router.get("/post_ids", response_model=PostIDsResponse)
async def get_post_ids():
    ids = get_all_post_ids() 
    return PostIDsResponse(ids=ids) 

# Added By: Vatsal Gandhi
@router.get("/post/{post_id}", response_model=GetPostResponse)
async def retrieve_post(post_id: str):
    result = await get_mastodon_post(post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return GetPostResponse(
        message="Post found",
        id=result["id"],
        content=result["content"][3:-4],  
        created_at=result["created_at"]
    )

# Added By: Urvashi Kohale
@router.delete("/post/{post_id}", response_model=DeletePostResponse)
async def delete_post(post_id: str):
    success = await delete_mastodon_post(post_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete post")
    
    return DeletePostResponse(message="Post deleted")