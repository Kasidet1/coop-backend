from pydantic import BaseModel
from datetime import date
from typing import Optional, List


# ======================
# User
# ======================

class UserCreate(BaseModel):
    username: str
    password: str
    role: str


class User(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


# ======================
# Login
# ======================

class Login(BaseModel):
    username: str
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
    username: str
    phone: str
    semester: str
    teacher_id: Optional[int] = None


class StudentRegister(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    username: str
    phone: str
    semester: str
    password: str


class Student(BaseModel):
    id: int
    student_id: str
    first_name: str
    last_name: str
    faculty: str
    major: str
    username: str
    phone: str
    semester: str
    teacher_id: Optional[int] = None

    class Config:
        from_attributes = True


# ======================
# Teacher
# ======================

class TeacherCreate(BaseModel):
    rank: str
    first_name: str
    last_name: str
    email: str
    role: str


class Teacher(BaseModel):
    id: int
    rank: str
    first_name: str
    last_name: str
    email: str
    role: str

    class Config:
        from_attributes = True


# ======================
# Company
# ======================

class CompanyCreate(BaseModel):
    company_name: str
    address: str
    county: str
    industry: str
    allowance: str
    accommodation: str
    shuttle: str
    welfare: str


class Company(BaseModel):
    id: int
    company_name: str
    address: str
    county: str
    industry: str
    allowance: str
    accommodation: str
    shuttle: str
    welfare: str

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

    class Config:
        from_attributes = True


# ======================
# Supervision
# ======================

class SupervisionCreate(BaseModel):
    teacher_id: int
    student_id: int
    company_id: int
    date: date
    type: str
    note: str
    status: str


class Supervision(BaseModel):
    id: int
    teacher_id: int
    student_id: int
    company_id: int
    date: date
    type: str
    note: str
    status: str

    class Config:
        from_attributes = True


# ======================
# Teacher Supervision View
# ======================

class TeacherSupervision(BaseModel):

    teacher_first_name: str
    teacher_last_name: str

    company_name: str
    county: str
    industry: str

    student_id: str

    student_first_name: str
    student_last_name: str

    date: date
    type: str
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
    supervisions: int


class TeacherDashboard(BaseModel):
    students: int
    supervision_count: int
    supervisions: List[TeacherSupervision]


# ======================
# Assign Teacher
# ======================

class AssignTeacher(BaseModel):
    student_id: int
    teacher_id: int
