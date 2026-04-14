from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from . import schemas
from .database import engine, Base, get_db
from . import models, crud
from .auth import create_access_token
from .auth import get_current_user
from .auth import require_role
import shutil
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Coop backend"}


# ======================
# STUDENTS (Admin Only)
# ======================

@app.get("/students")
def read_students(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.get_students(db)


@app.post("/students")
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.create_student(db, student)


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.update_student(db, student_id, student)


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.delete_student(db, student_id)


# ======================
# AUTH
# ======================

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):

    db_user = crud.login_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "role": db_user.role
    }


# ======================
# STUDENT LOGIN
# ======================

@app.post("/student/login")
def student_login(
    data: schemas.StudentLogin,
    db: Session = Depends(get_db)
):

    student = crud.student_login(
        db,
        data.student_id,
        data.password
    )

    if not student:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": student.student_id,
            "role": "student"
        }
    )

    return {
        "access_token": access_token,
        "role": "student"
    }


# ======================
# APPLICATION
# ======================

@app.post("/apply")
def apply_company(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.create_application(db, application)


@app.get("/applications")
def read_applications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.get_applications(db)


@app.put("/applications/{application_id}/approve")
def approve_application(
    application_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.update_application_status(db, application_id, "approved")


@app.put("/applications/{application_id}/reject")
def reject_application(
    application_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.update_application_status(db, application_id, "rejected")


# ======================
# Upload PDF
# ======================

UPLOAD_DIR = "uploads"


@app.post("/upload-pdf")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}


# ======================
# SUPERVISION (Teacher)
# ======================

@app.post("/supervision")
def create_supervision(
    supervision: schemas.SupervisionCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):
    return crud.create_supervision(db, supervision)


@app.get("/supervision")
def read_supervision(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):
    return crud.get_supervisions(db)


# ======================
# TEACHER STUDENTS
# ======================

@app.get("/teacher/students")
def teacher_students(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):
    return crud.get_teacher_students(db, user["sub"])


# ======================
# ADMIN DASHBOARD
# ======================

@app.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.admin_dashboard(db)


# ======================
# TEACHER DASHBOARD
# ======================

@app.get("/teacher/dashboard")
def teacher_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):
    return crud.teacher_dashboard(db, user["sub"])


# ======================
# ASSIGN TEACHER
# ======================

@app.put("/assign-teacher")
def assign_teacher(
    data: schemas.AssignTeacher,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.assign_teacher(
        db,
        data.student_id,
        data.teacher_id
    )


# ======================
# COMPANY CRUD
# ======================

@app.post("/companies")
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.create_company(db, company)


@app.get("/companies")
def get_companies(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return crud.get_companies(db)


@app.put("/companies/{company_id}")
def update_company(
    company_id: int,
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.update_company(db, company_id, company)


@app.delete("/companies/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    return crud.delete_company(db, company_id)