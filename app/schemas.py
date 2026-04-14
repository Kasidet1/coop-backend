from pydantic import BaseModel
from datetime import date
from typing import Optional, List


# ======================
# User
# ======================

class UserCreate(BaseModel):
    email: str
    password: str
    role: str


class User(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True


# ======================
# Login
# ======================

class Login(BaseModel):
    email: str
    password: str


# ======================
# Student
# ======================

class StudentCreate(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    teacher_id: Optional[int] = None


class StudentRegister(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    password: str


class Student(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True


# ======================
# Student Login
# ======================

class StudentLogin(BaseModel):
    student_id: str
    password: str


# ======================
# Teacher
# ======================

class TeacherCreate(BaseModel):
    teacher_id: str
    first_name: str
    last_name: str
    faculty: str


class Teacher(BaseModel):
    id: int
    teacher_id: str
    first_name: str
    last_name: str
    faculty: str

    class Config:
        from_attributes = True


# ======================
# Company
# ======================

class CompanyCreate(BaseModel):
    company_name: str
    address: str
    industry: str


class Company(BaseModel):
    id: int
    company_name: str
    address: str
    industry: str

    class Config:
        from_attributes = True


# ======================
# Application
# ======================

class ApplicationCreate(BaseModel):
    student_id: int
    company_id: int


class Application(BaseModel):
    id: int
    student_id: int
    company_id: int
    status: str
    file: Optional[str] = None

    class Config:
        from_attributes = True


# ======================
# Supervision
# ======================

class SupervisionCreate(BaseModel):
    teacher_id: int
    student_id: int
    date: date
    type: str
    note: str
    status: str


class Supervision(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    date: date
    type: str
    note: str
    status: str

    class Config:
        from_attributes = True


# ======================
# Dashboard
# ======================

class AdminDashboard(BaseModel):
    students: int
    companies: int
    applications: int


class TeacherDashboard(BaseModel):
    students: int
    supervisions: List[Supervision]


# ======================
# Assign Teacher
# ======================

class AssignTeacher(BaseModel):
    student_id: int
    teacher_id: int