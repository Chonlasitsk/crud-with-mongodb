from fastapi import APIRouter, status, Request
from fastapi.exceptions import HTTPException
from typing import List
from bson import ObjectId

from simplecrudapi import schemas

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", 
          response_description="Create a new User", 
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False, 
          response_model=schemas.UserOutput)
async def create_student(request: Request, user: schemas.User) -> schemas.UserOutput:
    user_dict = user.model_dump()
    try:
        user_added = await request.app.db["user"].insert_one(user_dict)
        res = await request.app.db["user"].find_one({"_id": user_added.inserted_id})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while inserting data into mongodb")
    return res

@router.get("/", 
         response_description="List all User", 
         response_model_by_alias=False, 
         status_code=status.HTTP_200_OK, 
         response_model=List[schemas.UserOutput])
async def get_users(request: Request) -> List[schemas.UserOutput]:
    users = await request.app.db["user"].find().to_list()
    return users

@router.get("",
         response_description="Get some user",
         response_model_by_alias=False,
         status_code=status.HTTP_200_OK,
         response_model=List[schemas.UserOutput])
async def get_some_user(request: Request, skip: int = 0, limit: int = 5) -> List[schemas.UserOutput]:
    res = await request.app.db["user"].find().skip(skip).limit(limit).to_list()
    return res

@router.get("/{id}", 
         response_description="Get a single User by id", 
         response_model_by_alias=False, 
         status_code=status.HTTP_200_OK, 
         response_model=schemas.UserOutput)
async def get_users_with_id(request: Request, id: str) -> schemas.UserOutput:
    try:
        user = await request.app.db["user"].find_one({"_id": ObjectId(id)})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while querying from mongodb")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
    return user

@router.put("/{id}", 
         response_description="Update a User", 
         response_model_by_alias=False, 
         status_code=status.HTTP_200_OK,
         response_model=schemas.UserOutput 
         )
async def update_user_with_id(request: Request, id: str, user: schemas.UserUpdate) -> schemas.UserOutput:
    user_dict = user.model_dump()
    user_to_update = {k:v for k, v in user_dict.items() if v is not None}
    try:
        if user_to_update:
            await request.app.db["user"].update_one({"_id": ObjectId(id)}, {"$set": user_to_update})

        res = await request.app.db["user"].find_one({"_id": ObjectId(id)})
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID format invalid") 
    return res

@router.delete("/{id}",
            response_description="Delete a User",
            status_code=status.HTTP_200_OK,
            )
async def delete_user_with_id(request: Request, id: str):
    try:    
        res = await request.app.db["user"].delete_one({"_id": ObjectId(id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while deleting in database")
    if not res.deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID not found")
    return {"message": "delete completed"}