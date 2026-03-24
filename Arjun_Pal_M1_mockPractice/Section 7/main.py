from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory database
students = []

# Simple Function (for testing)
def add_numbers(a, b):
    return a + b

# API Endpoint 1 (Home)
# 
@app.get("/")
def home():
    return {"message": "FastAPI is running successfully"}

# API Endpoint 2 (Add Student)
@app.post("/students")
def add_student(student: dict):
    students.append(student)
    return {"message": "Student added", "data": student}

# API Endpoint 3 (Get Students)
@app.get("/students")
def get_students():
    return students

# API Endpoint 4 (Get by ID)
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]