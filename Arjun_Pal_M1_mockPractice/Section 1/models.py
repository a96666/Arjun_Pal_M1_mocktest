from pydantic import BaseModel, EmailStr
from typing import Optional
# pydantic is used for automatic data validation of user
class Student(BaseModel):
    id:int
    name:str
    age:int
    course:str
    email:Optional[EmailStr]=None
