from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
import uuid

from simplecrudapi.odm_schemas import Profile, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/", 
            response_description="Create a new Profile", 
            status_code=status.HTTP_201_CREATED,
            response_model_by_alias=False,
            response_model=Profile
            )
async def create_profile(profile: Profile) -> Profile:
    profile_dict = profile.model_dump()
    profile_dict["id"] = str(uuid.uuid4())
    profile_document = Profile(**profile_dict)
    try:
        res = await Profile.insert_one(profile_document)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while inserting into database")
    return res

@router.get("/",
            response_description="Get a all profiles",
            status_code=status.HTTP_200_OK,
            response_model_by_alias=False,
            response_model=List[Profile],
            )
async def get_all_profile() -> List[Profile]:
    try:
        res = await Profile.find().to_list()
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while getting data from database")
    return res

@router.get("/{id}",
            response_description="Get a single profile",
            status_code=status.HTTP_200_OK,
            response_model_by_alias=False,
            response_model=Profile)
async def get_profile(id: str):
    try:
        res = await Profile.find_one(Profile.id == id)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while getting data from database")
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    return res

@router.put("/{id}",
            response_description="Update a single profile",
            status_code=status.HTTP_200_OK,
            response_model_by_alias=False,
            response_model=ProfileUpdate)
async def update_profile(id: str, profile: ProfileUpdate) -> ProfileUpdate:
    try:
        profile_to_update = await Profile.find_one(Profile.id == id)
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while getting data from database")

    if not profile_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")

    for key in profile.model_fields.keys():
        value_to_update = getattr(profile, key)
        if value_to_update is not None:
            setattr(profile_to_update, key, value_to_update)

    await profile_to_update.save()    
    return profile_to_update

@router.delete("/{id}",
               response_description="Delete a single profile",
               status_code=status.HTTP_200_OK)
async def delete_profile(id: str):
    try:
        profile_to_delete = await Profile.find_one(Profile.id == id)
    except Exception as e:
       print("Error: ", e)
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while getting data from database")
     
    if not profile_to_delete:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    await profile_to_delete.delete()
    return {"message": "delete completed"}