from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Student, Professor

app = FastAPI()
Base.metadata.create_all(bind=engine) 
def get_db():
    # Create new db session, its an obj of sqlalchemy.orm.Session
    db = SessionLocal()  # Calls fn session maker  which will ask the engine for connection -> engine create a connection
    try: 
        yield db
        # one session is running pause execution wail until the route is finished resume execution
    finally:
        db.close()
# post request -> fastapi call get_db(), db = SessionLocal(), pause execution, db is given to route fun
# route fn starts running, wait until route fun is finished, after route finishes, fastAPI 
@app.post("/students")
def create_student(name: str, age:int, course:str, db: Session = Depends(get_db)):
    student = Student(name = name, hage = age, course = course)
    db.add(student) #prepare it to be inserted into db not immediate
    db.commit() # convert ORM obj into SQL INSERT commands, then it will send SQL INSERT
    db.refresh(student) # reload the obj in database
    return student # server response

@app.get("/students")
def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all() #JSON dictionary is server response
# build a SELECT query  for student table, get all rows from Student table, convert each row into student object

@app.put("/students/{student_id}")
def update_student(student_id: int, name: str, age: int, course: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first() # filter will run where clause compares database == user request,
    # first() return only one value at a time .all()[0]. Works like LIMIT Clause 
    # Stored in dictionary format
    student.name = name
    student.age = age
    student.course = course
    db.commit()
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    db.delete(student)
    db.commit()
    return {"message": "Student deleted"}



@app.post("/professors")
def create_professor(name: str, age: int, course: str, db: Session = Depends(get_db)):
    professor = Professor(name=name, age=age, course=course)
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

@app.get("/professors")
def read_professors(db: Session = Depends(get_db)):
    return db.query(Professor).all()

@app.put("/professors/{professor_id}")
def update_professor(professor_id: int, name: str, age: int, course: str, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if professor:
        professor.name = name
        professor.age = age
        professor.course = course
        db.commit()
        db.refresh(professor)
        return professor
    else:
        return {"message": "Professor not found"}

@app.delete("/professors/{professor_id}")
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.query(Professor).filter(Professor.id == professor_id).first()

    if professor:
        db.delete(professor)
        db.commit()
        return {"message": "Professor deleted"}
    else:
        return {"message": "Professor not found"}