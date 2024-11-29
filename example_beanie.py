from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field, BaseModel
from typing import Optional
import asyncio
import os

class Book(Document):
    title: str = Field(...)
    author: str = Field(...)
    price: float = Field(...)
    class Settings:
        name = "books"

class BookView(BaseModel):
    title: str
    author: str

async def insert_into_database():
    mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(database=mongodb_client.test_beanie, document_models=[Book])
    
    # create instance of Book document class to insert into database
    book1 = Book(title="King landing 1", author="Pault alonto", price=200)
    book2 = Book(title="Land of king", author="Robert Molly", price=400)
    book3 = Book(title="The lord of the ring", author="Mark watney", price=600)
    book4 = Book(title="The last of us 1", author="Mike Bokke", price=4040)
    book5 = Book(title="Sometime", author="Molly", price=7800)

    ## insert single document into database by call "insert()" instance method ##
    # await book1.insert()
    # await book2.insert()
    
    ## insert single document into database by call "insert_one()" Class method ##
    # await Book.insert_one(document=book1)

    ## insert multiple documents into database by call "insert_many()" class method ##
    await Book.insert_many(documents=[book1, book2, book3, book4, book5])

async def query():
   mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
   await init_beanie(database=mongodb_client.test_beanie, document_models=[Book])

   # finding multiple documents in the database is to call "find()" class method with some search critiria (like WHERE in SQL)
   res_document = await Book.find().to_list()

   # finding multiple documents in the database with conditions
   res_document = await Book.find(Book.price > 300).to_list()

   # finding multiple documents in the database with conditions and projection (like SELECT command in SQL)
   res_document = await Book.find(Book.price > 300).project(BookView).to_list()
   res_document = await Book.find(Book.title == "The lord of the ring").project(BookView).to_list()
   
   # Other MongoDB query operator can be used from "beanie.operators"
   from beanie.operators import In
   res_document = await Book.find(In(Book.title, ["The last of us", "Sometime"])).to_list()

   # finding mulitple documents more than conditions 
   res_document = await Book.find(Book.title == "King landing 1", Book.price > 200).to_list()

   # Sorting, you can sorting by call "sort()" method 
   # Pass it one or multiple fields to sort by. You may optionally specify a + or - (denoting ascending and descending respectively).
   res_document = await Book.find().sort(-Book.price).to_list()

   # Skip and limit
   res_document = await Book.find().limit(2).to_list()
   res_document = await Book.find().skip(3).to_list()
    
async def update():
    mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(database=mongodb_client.test_beanie, document_models=[Book])
    # use "save()" instance method to update 
    book_to_update = await Book.find_one(Book.title == "like something forever 2")
    print(book_to_update.model_dump())
    book_to_update.title = "like something forever 2"
    book_to_update.price = 8500
    await book_to_update.save()

    # Native MongoDB syntax is also supported:
    await Book.find_one(Book.title == "like something forever 2").update({"$set": {Book.price: 20000}})

async def delete():
    mongodb_client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    await init_beanie(database=mongodb_client.test_beanie, document_models=[Book])

    book_to_delete = await Book.find_one(Book.title == "like something forever 2")
    await book_to_delete.delete()

if __name__ == "__main__":
    #asyncio.run(insert_into_database())
    #asyncio.run(query())
    #asyncio.run(update())
    asyncio.run(delete())