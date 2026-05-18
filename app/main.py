from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import shutil
import os

from . import schemas, crud
from .database import get_db
from .auth import (
    create_access_token,
    get_current_user,
    require_role
)

app = FastAPI()

# ======================
# CORS
# ======================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# ROOT
# ======================

@app.get("/")
def root():

    return {
        "message": "Coop backend"
    }


# ======================
# AUTH
# ======================

@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(
        db,
        user
    )


@app.post("/login")
def login(
    user: schemas.Login,
    db: Session = Depends(get_db)
):

    db_user = crud.login_user(
        db,
        user.username,
        user.password
    )

    if not db_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.username,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "role": db_user.role
    }


# ======================
# STUDENTS
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

    return crud.create_student(
        db,
        student
    )


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.update_student(
        db,
        student_id,
        student
    )


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.delete_student(
        db,
        student_id
    )


# ======================
# STUDENT PROFILE
# ======================

@app.get("/student/me")
def get_student_profile(
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):

    student = crud.get_student_profile(
        db,
        user["sub"]
    )

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put("/student/me")
def update_student_profile(
    student_data: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role("student"))
):

    student = crud.update_student_profile(
        db,
        user["sub"],
        student_data
    )

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ======================
# APPLICATION
# ======================

@app.post("/apply")
def apply_company(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return crud.create_application(
        db,
        application
    )


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

    return crud.update_application_status(
        db,
        application_id,
        "approved"
    )


@app.put("/applications/{application_id}/reject")
def reject_application(
    application_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.update_application_status(
        db,
        application_id,
        "rejected"
    )


# ======================
# UPLOAD PDF
# ======================

UPLOAD_DIR = "uploads"


@app.post("/upload-pdf")
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "filename": file.filename
    }


# ======================
# SUPERVISION
# ======================

@app.post("/supervision")
def create_supervision(
    supervision: schemas.SupervisionCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    return crud.create_supervision(
        db,
        supervision
    )


@app.get("/supervision")
def read_supervision(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    return crud.get_supervisions(db)


# ======================
# TEACHER
# ======================

@app.get("/teacher/students")
def teacher_students(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    teacher = crud.get_teacher_by_username(
        db,
        user["sub"]
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return crud.get_teacher_students(
        db,
        teacher.id
    )


@app.get("/teacher/dashboard")
def teacher_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    teacher = crud.get_teacher_by_username(
        db,
        user["sub"]
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return crud.teacher_dashboard(
        db,
        teacher.id
    )


@app.get("/teacher/supervisions")
def teacher_supervisions(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    teacher = crud.get_teacher_by_username(
        db,
        user["sub"]
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return crud.get_teacher_supervisions(
        db,
        teacher.id
    )


# ======================
# TEACHER PROFILE
# ======================

@app.get("/teacher/me")
def get_my_profile(
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    teacher = crud.get_teacher_profile(
        db,
        user["sub"]
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


@app.put("/teacher/me")
def update_my_profile(
    teacher_data: schemas.TeacherUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role("teacher"))
):

    teacher = crud.update_teacher_profile(
        db,
        user["sub"],
        teacher_data
    )

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


# ======================
# ADMIN
# ======================

@app.get("/admin/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.admin_dashboard(db)


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
# COMPANIES
# ======================

@app.post("/companies")
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.create_company(
        db,
        company
    )


# ======================
# SEARCH + FILTER COMPANY
# ======================

@app.get("/companies")
def get_companies(
    search: str = None,
    county: str = None,
    industry: str = None,
    allowance: str = None,
    accommodation: str = None,
    shuttle: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return crud.get_companies(
        db,
        search,
        county,
        industry,
        allowance,
        accommodation,
        shuttle
    )


@app.put("/companies/{company_id}")
def update_company(
    company_id: int,
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.update_company(
        db,
        company_id,
        company
    )


@app.delete("/companies/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    return crud.delete_company(
        db,
        company_id
    )
