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
