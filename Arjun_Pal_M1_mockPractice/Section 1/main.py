from fastapi import FastAPI, HTTPException
from typing import List, Optional
from models import Student # class(BaseModel)
from database import students #empty list
app=FastAPI(
    title="Student Management API",
    description="A simple REST API using FastAPI (CRUD + Filter + Search)",
    version="1.0.0"
            )

@app.get("/")
def read_root():
    return {"msg":"Welcome to Student management Api"}
@app.get("/about")
def about():
    return {"info":"Fast Api"}

#create student post
@app.post("/students",response_model=Student)
def create_student(student:Student): #student=request body(json)
    students.append(student)
    return student



#get all student
@app.get("/students",response_model=List[Student])
def get_student():
    return students


# get Student by id(path parameter)
@app.get("/students/{student_id}",response_model=Student)
def get_student(student_id:int):
    if student_id<0 or student_id>=len(students):
        raise HTTPException(status_code=404,
                            detail="student not found")
    return students[student_id]


# update Student(Put)
@app.put("/students/{student_id}")
def update_student(student_id:int,updated_student:Student):
    if student_id>0 and student_id<=len(students):
        raise HTTPException(
            status_code=404,
            detail="not found"
        )
    students[student_id]=updated_student


    return {
        "msg":"update successfull",
        "data":updated_student

    }

# UPDATE Student (PUT)
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    #updated_Student store the new request body data
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = updated_student

    return {
        "message": "Student updated successfully",
        "data": updated_student
    }

# Filter
@app.get("/filter") 
def filter_students(course: Optional[str] = None):
    if not course:
        return {"message"}

    filtered = [
        s for s in students
        if s.course.lower() == course.lower()
    ]
    return {
        "count" : len(filtered),
        "students": filtered
    }
@app.get("/search")
def search_student(name:str):
    result=[
        s for s in students if name.lower() in s.name.lower()
    ]

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No student found with this name"
        )
    
    return{
        "Count":len(result),
        "Serached":result
    }
